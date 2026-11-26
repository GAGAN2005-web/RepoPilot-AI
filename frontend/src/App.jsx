import { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import {
  Send,
  Loader2,
  Sparkles,
  FileCode2,
  ChevronRight,
  Plus,
  MessageSquare,
  ExternalLink,
  AlertCircle,
} from "lucide-react";

import {
  registerRepository,
  sendMessage,
  getConversation,
  getConversations,
} from "./services/api";

import "./App.css";

function App() {
  const [repoUrl, setRepoUrl] = useState("");
  const [repository, setRepository] = useState(null);

  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);

  const [conversationId, setConversationId] = useState(null);
  const [conversations, setConversations] = useState([]);
  const [loadingRepo, setLoadingRepo] = useState(false);
  const [loadingChat, setLoadingChat] = useState(false);

  const [error, setError] = useState("");

  const loadConversations = async (repositoryId) => {
  try {
    const data = await getConversations(repositoryId);
    setConversations(data);
  } catch (err) {
    console.error("Failed to load conversations:", err);
  }
};

const connectRepository = async () => {
  if (!repoUrl.trim() || loadingRepo) return;

  setLoadingRepo(true);
  setError("");

  try {
    const data = await registerRepository(repoUrl.trim());

    setRepository(data);
    setMessages([]);
    setConversationId(null);

    await loadConversations(data.id);


  } catch (err) {
    const detail = err.response?.data?.detail;

    if (Array.isArray(detail)) {
      setError(
        detail
          .map((item) => item.msg)
          .filter(Boolean)
          .join(". ")
      );
    } else {
      setError(
        detail ||
          "Could not connect to the repository."
      );
    }
  }
};

  const askQuestion = async () => {
    if (!question.trim() || !repository || loadingChat) return;

    const currentQuestion = question.trim();

    setQuestion("");
    setError("");

    setMessages((previous) => [
      ...previous,
      {
        role: "user",
        content: currentQuestion,
      },
    ]);

    setLoadingChat(true);

    try {
      const data = await sendMessage(
        repository.id,
        currentQuestion,
        conversationId
      );

      setConversationId(data.conversation_id);
      await loadConversations(repository.id);

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content: data.answer,
          sources: data.sources || [],
        },
      ]);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Something went wrong while processing your question."
      );
    } finally {
      setLoadingChat(false);
    }
  };

  const handleQuestionKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      askQuestion();
    }
  };

  const startNewConversation = () => {
    setMessages([]);
    setConversationId(null);
    setQuestion("");
    setError("");
  };

  const openConversation = async (id) => {
  if (loadingChat || id === conversationId) return;

  setError("");

  try {
    const data = await getConversation(id);

    setConversationId(data.id);

    setMessages(
      data.messages.map((message) => ({
        role: message.role,
        content: message.content,
        sources: message.source_references || [],
      }))
    );
  } catch (err) {
    setError(
      err.response?.data?.detail ||
        "Could not load this conversation."
    );
  }
};

  const useSuggestion = (text) => {
    setQuestion(text);
  };

  return (
    <div className="app-shell">
      {/* SIDEBAR */}

      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">
            <Sparkles size={18} />
          </div>

          <div>
            <div className="brand-name">RepoPilot</div>
            <div className="brand-version">
              AI CODE EXPLORER
            </div>
          </div>
        </div>

        <button
          className="new-chat-btn"
          onClick={startNewConversation}
        >
          <Plus size={17} />
          New conversation
        </button>

        <div className="sidebar-section">
          <div className="section-label">
            REPOSITORY
          </div>

          {repository ? (
            <div className="repo-card">
              <div className="repo-icon">
                <FileCode2 size={17} />
              </div>

              <div className="repo-details">
                <strong>
                  {repository.owner}/{repository.name}
                </strong>

                <span>
                  {repository.language || "Repository"}
                </span>
              </div>

              <div className="status-dot" />
            </div>
          ) : (
            <div className="empty-repo">
              <FileCode2 size={18} />
              <span>No repository connected</span>
            </div>
          )}
        </div>

        <div className="sidebar-section history-section">
          <div className="section-label">
            CONVERSATIONS
          </div>

          {conversations.length === 0 ? (
            <div className="history-item">
              <MessageSquare size={15} />
              <span>No conversations yet</span>
            </div>
          ) : (
            conversations.map((conversation) => (
              <button
                key={conversation.id}
                className={`history-item ${
                  conversation.id === conversationId ? "active" : ""
                }`}
                onClick={() => openConversation(conversation.id)}
              >
                <MessageSquare size={15} />

                <span>
                  {conversation.title ||
                    `Conversation #${conversation.id}`}
                </span>
              </button>
            ))
          )}
        </div>

        <div className="sidebar-footer">
          <div className="footer-line">
            <span>Backend</span>

            <span className="online">
              <i />
              Connected
            </span>
          </div>

          <div className="footer-line muted">
            FastAPI · ChromaDB · Ollama
          </div>
        </div>
      </aside>

      {/* MAIN */}

      <main className="main-area">
        <header className="topbar">
          <div>
            <div className="topbar-title">
              {repository
                ? repository.name
                : "Repository Intelligence"}
            </div>

            <div className="topbar-subtitle">
              {repository
                ? "Ask questions about your codebase"
                : "Understand any GitHub repository with AI"}
            </div>
          </div>

          {repository && repository.url && (
            <a
              href={repository.url}
              target="_blank"
              rel="noreferrer"
              className="github-link"
            >
              View on GitHub
              <ExternalLink size={13} />
            </a>
          )}
        </header>

        {/* WELCOME SCREEN */}

        {!repository ? (
          <section className="welcome-screen">
            <div className="welcome-content">
              <div className="hero-icon">
                <Sparkles size={28} />
              </div>

              <p className="eyebrow">
                REPOSITORY INTELLIGENCE
              </p>

              <h1>
                Understand your codebase
                <br />
                <span>
                  without digging through every file.
                </span>
              </h1>

              <p className="hero-description">
                Connect a GitHub repository and ask questions
                about its implementation, architecture, files,
                models, and dependencies.
              </p>

              <div className="repo-input-wrapper">
                <FileCode2 size={19} />

                <input
                  value={repoUrl}
                  onChange={(event) =>
                    setRepoUrl(event.target.value)
                  }
                  onKeyDown={(event) => {
                    if (event.key === "Enter") {
                      connectRepository();
                    }
                  }}
                  placeholder="https://github.com/owner/repository"
                />

                <button
                  onClick={connectRepository}
                  disabled={
                    loadingRepo || !repoUrl.trim()
                  }
                >
                  {loadingRepo ? (
                    <>
                      <Loader2
                        size={17}
                        className="spin"
                      />
                      Connecting
                    </>
                  ) : (
                    <>
                      Connect
                      <ChevronRight size={16} />
                    </>
                  )}
                </button>
              </div>

              <div className="feature-row">
                <div>
                  <FileCode2 size={16} />
                  <span>Code-aware search</span>
                </div>

                <div>
                  <Sparkles size={16} />
                  <span>Grounded answers</span>
                </div>

                <div>
                  <MessageSquare size={16} />
                  <span>Conversation history</span>
                </div>
              </div>

              {error && (
                <div className="error-box welcome-error">
                  <AlertCircle size={16} />
                  {error}
                </div>
              )}
            </div>
          </section>
        ) : (
          /* CHAT */

          <section className="chat-layout">
            <div className="chat-container">
              {messages.length === 0 ? (
                <div className="chat-empty">
                  <div className="chat-empty-icon">
                    <Sparkles size={22} />
                  </div>

                  <h2>
                    Ask about {repository.name}
                  </h2>

                  <p>
                    Explore implementation details, files,
                    models, dependencies, or repository
                    metadata.
                  </p>

                  <div className="suggestions">
                    <button
                      onClick={() =>
                        useSuggestion(
                          "Where is the machine learning model loaded?"
                        )
                      }
                    >
                      Where is the machine learning model loaded?
                    </button>

                    <button
                      onClick={() =>
                        useSuggestion(
                          "Show me the complete app.py file."
                        )
                      }
                    >
                      Show me the complete app.py file
                    </button>

                    <button
                      onClick={() =>
                        useSuggestion(
                          "How many stars does this repository have?"
                        )
                      }
                    >
                      How many stars does this repository have?
                    </button>
                  </div>
                </div>
              ) : (
                <div className="messages">
                  {messages.map((message, index) => (
                    <div
                      className={`message-row ${message.role}`}
                      key={index}
                    >
                      <div className="message-avatar">
                        {message.role === "user" ? (
                          "G"
                        ) : (
                          <Sparkles size={15} />
                        )}
                      </div>

                      <div className="message-body">
                        <div className="message-role">
                          {message.role === "user"
                            ? "You"
                            : "RepoPilot"}
                        </div>

                        <div className="message-content">
                          {message.role ===
                          "assistant" ? (
                            <ReactMarkdown>
                              {message.content}
                            </ReactMarkdown>
                          ) : (
                            <p>{message.content}</p>
                          )}
                        </div>

                        {message.sources &&
                          message.sources.length > 0 && (
                            <div className="sources">
                              <div className="sources-label">
                                SOURCES
                              </div>

                              <div className="source-list">
                                {message.sources.map(
                                  (
                                    source,
                                    sourceIndex
                                  ) => (
                                    <div
                                      className="source-card"
                                      key={sourceIndex}
                                    >
                                      <FileCode2
                                        size={14}
                                      />

                                      <div>
                                        <strong>
                                          {source.path}
                                        </strong>

                                        <span>
                                          {source.language ||
                                            "code"}{" "}
                                          · chunk{" "}
                                          {
                                            source.chunk_index
                                          }
                                        </span>
                                      </div>
                                    </div>
                                  )
                                )}
                              </div>
                            </div>
                          )}
                      </div>
                    </div>
                  ))}

                  {loadingChat && (
                    <div className="message-row assistant">
                      <div className="message-avatar">
                        <Sparkles size={15} />
                      </div>

                      <div className="message-body">
                        <div className="message-role">
                          RepoPilot
                        </div>

                        <div className="typing">
                          <span />
                          <span />
                          <span />
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              )}

              {error && messages.length > 0 && (
                <div className="error-box">
                  <AlertCircle size={16} />
                  {error}
                </div>
              )}

              {/* COMPOSER */}

              <div className="composer">
                <textarea
                  value={question}
                  onChange={(event) =>
                    setQuestion(event.target.value)
                  }
                  onKeyDown={handleQuestionKeyDown}
                  placeholder="Ask anything about this repository..."
                  rows={1}
                  disabled={loadingChat}
                />

                <button
                  className="send-btn"
                  onClick={askQuestion}
                  disabled={
                    !question.trim() || loadingChat
                  }
                >
                  {loadingChat ? (
                    <Loader2
                      size={18}
                      className="spin"
                    />
                  ) : (
                    <Send size={18} />
                  )}
                </button>
              </div>

              <div className="composer-hint">
                Enter to send · Shift + Enter for a new line
              </div>
            </div>
          </section>
        )}
      </main>
    </div>
  );
}

export default App;