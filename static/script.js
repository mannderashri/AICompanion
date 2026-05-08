document.addEventListener('DOMContentLoaded', () => {
      // 1. NAVIGATION LOGIC
                              const navItems = document.querySelectorAll('.nav-item');
      const sections = document.querySelectorAll('.view-section');

                              navItems.forEach(item => {
                                        item.addEventListener('click', (e) => {
                                                      e.preventDefault();
                                                      const targetId = item.getAttribute('data-view');

                                                                          // Update Nav Active State
                                                                          navItems.forEach(ni => ni.classList.remove('active'));
                                                      item.classList.add('active');

                                                                          // Switch Sections
                                                                          sections.forEach(sec => {
                                                                                            sec.classList.remove('active');
                                                                                            if(sec.id === targetId) sec.classList.add('active');
                                                                          });
                                        });
                              });

                              // 2. CHAT SIMULATION
                              const chatInput = document.getElementById('chat-input');
      const sendBtn = document.getElementById('send-btn');
      const chatHistory = document.getElementById('chat-history');
      const thinkingMsg = document.getElementById('thinking-msg');
      const thinkingStrip = document.querySelector('.thinking-strip');

                              function addMessage(text, sender = 'user') {
                                        const msgDiv = document.createElement('div');
                                                       msgDiv.className = `message ${sender}-message`;

          const avatar = sender === 'ai' ? '<div class="msg-avatar ai-avatar"><i data-lucide="bot"></i></div>' : '<div class="msg-avatar user-avatar"><i data-lucide="user"></i></div>';
                                        const senderName = sender === 'ai' ? 'AI Companion <span class="sender-badge">CORE v2.4</span>' : 'You';
                                        const bubbleClass = sender === 'ai' ? 'ai-bubble' : 'user-bubble';

          msgDiv.innerHTML = `
                      ${avatar}
                                  <div class="msg-body">
                                                  <div class="msg-sender">${senderName}</div>
                                                                  <div class="${bubbleClass}">${text}</div>
                                                                              </div>
                                                                                      `;

          chatHistory.appendChild(msgDiv);
                                        chatHistory.scrollTop = chatHistory.scrollHeight;

          if(window.lucide) lucide.createIcons();
                              }

                              function simulateAIResponse() {
                                        thinkingStrip.style.display = 'flex';
                                        const thoughts = [
                                                      "Analyzing data patterns...",
                                                      "Consulting neural nodes...",
                                                      "Synthesizing response...",
                                                      "Finalizing neural output..."
                                                  ];

          let i = 0;
                                        const interval = setInterval(() => {
                                                      thinkingMsg.innerText = thoughts[i];
                                                      i++;
                                                      if(i >= thoughts.length) {
                                                                        clearInterval(interval);
                                                                        thinkingStrip.style.display = 'none';
                                                                        addMessage("I've processed your request. Based on the current repository context, everything is looking optimal. How else can I assist your workflow today?", 'ai');
                                                      }
                                        }, 800);
                              }

                              if(sendBtn) {
                                        sendBtn.addEventListener('click', () => {
                                                      const val = chatInput.value.trim();
                                                      if(val) {
                                                                        addMessage(val, 'user');
                                                                        chatInput.value = '';
                                                                                 setTimeout(simulateAIResponse, 500);
                                                      }
                                        });

          chatInput.addEventListener('keypress', (e) => {
                        if(e.key === 'Enter') sendBtn.click();
          });
                              }

                              // 3. QUIZ LOGIC
                              const options = document.querySelectorAll('.option-item');
      options.forEach(opt => {
                opt.addEventListener('click', () => {
                              const parent = opt.parentElement;
                              parent.querySelectorAll('.option-item').forEach(o => o.classList.remove('selected'));
                              opt.classList.add('selected');
                });
      });

                              // 4. INITIALIZE ICONS
                              if(window.lucide) lucide.createIcons();
});
