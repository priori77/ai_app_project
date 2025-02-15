from flask import Blueprint, request, jsonify
from services.vector_service import vector_service
from services.chat_service import ChatService
from flask_cors import cross_origin

bp = Blueprint('scenario', __name__)
chat_service = ChatService()

@bp.route('/', methods=['GET'])
def get_scenarios():
    """시나리오 목록 조회"""
    return jsonify({'scenarios': []})

@bp.route('/', methods=['POST'])
def create_scenario():
    """새로운 시나리오 생성"""
    data = request.get_json()
    return jsonify({'message': 'Scenario created successfully'}), 201

@bp.route('/<int:scenario_id>', methods=['GET'])
def get_scenario(scenario_id):
    """특정 시나리오 조회"""
    return jsonify({'scenario': {'id': scenario_id}})

@bp.route('/<int:scenario_id>/analyze', methods=['POST'])
def analyze_scenario(scenario_id):
    """시나리오 분석 (LAG + GPT)"""
    return jsonify({'analysis': 'Analysis result'})

@bp.route('/chat', methods=['POST'])
@cross_origin(supports_credentials=True)
def scenario_chat():
    """
    사용자로부터 '게임 내 스토리, 인물, 설정' 관련 질문을 받고,
    관련 문서를 벡터 검색(query)으로 가져와 문맥을 구성한 후,
    시스템 프롬프트와 함께 GPT에 전달하여 답변을 생성합니다.
    """
    try:
        data = request.get_json()
        question = data.get('message', '').strip()
        if not question:
            return jsonify({"success": False, "error": "메시지가 제공되지 않았습니다."}), 400

        # 1. 관련 문서 검색 (상위 3개)
        docs = vector_service.query(question, top_k=3)

        # 2. 검색된 문서들의 텍스트를 하나의 컨텍스트 스트링으로 조합
        context = ""
        for doc in docs.get("documents", [[]])[0]:
            context += doc + "\n\n"

        # 3. 시스템 프롬프트 구성
        # 가독성이 높은, 잘 구조화된 답변을 유도하는 프롬프트 추가
        system_prompt = (
            "너는 게임 내 스토리, 인물, 설정에 관한 시나리오 어시스턴트입니다. "
            "사용자에게 친절하고 가독성이 높으며, 명확하게 문단을 구분하여 답변해줘. "
            "필요한 경우 목록이나 표 형태로 정보를 정리하여 제공하고, 이해하기 쉽게 설명해줘.\n\n"
            f"문맥:\n{context}"
        )
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ]

        # 4. GPT 호출 (designer_type은 '범용'으로 설정)
        response = chat_service.create_chat_completion(messages, designer_type="범용")
        if response["success"]:
            return jsonify({"success": True, "message": response["message"]})
        else:
            return jsonify({"success": False, "error": response.get("error", "알 수 없는 오류")}), 500

    except Exception as e:
        print(f"Error in scenario_chat: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500
