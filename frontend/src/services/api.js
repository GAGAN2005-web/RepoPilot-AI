import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://127.0.0.1:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

export const registerRepository = async (url) => {
  const response = await api.post("/repositories", {
    url,
  });

  return response.data;
};

export const sendMessage = async (
  repositoryId,
  question,
  conversationId = null
) => {
  const payload = {
    question,
  };

  if (conversationId) {
    payload.conversation_id = conversationId;
  }

  const response = await api.post(
    `/repositories/${repositoryId}/chat`,
    payload
  );

  return response.data;
};

export const getConversation = async (conversationId) => {
  const response = await api.get(`/conversations/${conversationId}`);

  return response.data;
};


export const getConversations = async (repositoryId) => {
  const response = await api.get(
    `/repositories/${repositoryId}/conversations`
  );
  return response.data;
};

export default api;