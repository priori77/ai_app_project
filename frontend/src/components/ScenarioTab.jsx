import React, { useState, useEffect, useRef } from 'react';
import { 
  Box, 
  TextField, 
  Button, 
  Paper, 
  Typography, 
  List, 
  ListItem, 
  CircularProgress 
} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import { scenarioApi } from '../api/api'; // api.js에 scenarioApi 추가 필요

function ScenarioTab() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;
    const userMessage = input;
    setInput('');
    // 사용자 메시지 즉시 추가
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setLoading(true);

    try {
      const response = await scenarioApi.scenarioChat(userMessage);
      if (response.data.success) {
        setMessages(prev => [...prev, { role: 'assistant', content: response.data.message }]);
      } else {
        setMessages(prev => [...prev, { role: 'assistant', content: `오류: ${response.data.error}` }]);
      }
    } catch (error) {
      setMessages(prev => [...prev, { role: 'assistant', content: `네트워크 오류: ${error.message}` }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ maxWidth: '1200px', width: '100%', mx: 'auto', p: 3, height: 'calc(100vh - 100px)' }}>
      <Paper sx={{ p: 2, mb: 2, display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <Typography variant="h6">게임 시나리오 어시스턴트</Typography>
      </Paper>
      <Paper sx={{ height: 'calc(100vh - 250px)', overflow: 'auto', p: 2, mb: 2 }}>
        <List>
          {messages.map((msg, index) => (
            <ListItem 
              key={index} 
              sx={{ justifyContent: msg.role === 'user' ? 'flex-end' : 'flex-start' }}
            >
              <Paper sx={{ p: 2, backgroundColor: msg.role === 'user' ? 'primary.light' : 'grey.100' }}>
                <Typography variant="body1">{msg.content}</Typography>
              </Paper>
            </ListItem>
          ))}
          <div ref={messagesEndRef} />
        </List>
      </Paper>
      <Box sx={{ display: 'flex', gap: 1 }}>
        <TextField
          fullWidth
          variant="outlined"
          placeholder="게임 내 스토리, 인물, 설정에 관한 질문을 입력하세요..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          multiline
          maxRows={4}
          onKeyDown={(e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault();
              handleSend();
            }
          }}
          disabled={loading}
        />
        <Button
          variant="contained"
          onClick={handleSend}
          disabled={loading || !input.trim()}
          sx={{ height: '56px', minWidth: '80px', display: 'inline-flex', alignItems: 'center', justifyContent: 'center' }}
        >
          {loading ? <CircularProgress size={20} /> : (<><SendIcon /><span>전송</span></>)}
        </Button>
      </Box>
    </Box>
  );
}

export default ScenarioTab; 