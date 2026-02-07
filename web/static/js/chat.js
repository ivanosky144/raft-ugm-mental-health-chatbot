document.addEventListener("DOMContentLoaded", () => {
    const sidebar = document.getElementById("aspect-sidebar");
    const toggleBtn = document.getElementById("toggle-aspect-sidebar-btn");
    const chatWindow = document.getElementById("chat-window");
    const chatForm = document.getElementById("chat-form");
    const messageInput = document.getElementById("message-input");
    const newChatBtn = document.getElementById("new-chat-btn");
    const aspectList = document.getElementById("aspect-list");
    const conversationList = document.getElementById("conversation-list");
    const ALL_SECTIONS = [
        "Depression",
        "Anger",
        "Mania",
        "Anxiety",
        "Somatic",
        "Suicidal",
        "Psychosis",
        "Sleep Disturbance",
        "Memory",
        "Dissociation",
        "Substance Use",
        "Repetitive Thought"
    ];
    
    const SECTION_COLORS = {
        "Depression": "#3b82f6",
        "Anger": "#ef4444",
        "Mania": "#a855f7",
        "Anxiety": "#f59e0b",
        "Somatic": "#14b8a6",
        "Suicidal": "#dc2626",
        "Psychosis": "#6366f1",
        "Sleep Disturbance": "#0ea5e9",
        "Memory": "#22c55e",
        "Dissociation": "#eab308",
        "Substance Use": "#f97316",
        "Repetitive Thought": "#ec4899"
    };


    let currentChatId = null;
    const user_id = localStorage.getItem("user_id") || null;
        
    toggleBtn.addEventListener("click", () => {
        sidebar.classList.toggle("hidden");

        if (sidebar.classList.contains("hidden")) {
            toggleBtn.textContent = "⮜";
            toggleBtn.style.right = "40px";
        }
        else {
            toggleBtn.textContent = "⮞";
            toggleBtn.style.right = "300px";
        }
    });

    async function apiFetch(url, options = {}) {
        const res = await fetch(url, {
            headers: {"Content-Type": "application/json"},
            ...options,
        })
        return res.json();
    };

    function addMessage(text, sender = "bot") {
        const wrapper = document.createElement("div");
        wrapper.className = `chat-message ${sender}`;
        
        const msg = document.createElement("div");
        msg.className = "message";
        msg.textContent = text;

        wrapper.appendChild(msg);
        chatWindow.appendChild(wrapper);
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    function renderEmptyProgress() {
        aspectList.innerHTML = "";
    
        const TOTAL = 10;
    
        ALL_SECTIONS.forEach(section => {
            const color = SECTION_COLORS[section] || "#4caf50";
    
            const div = document.createElement("div");
            div.className = "aspect-item";
    
            div.innerHTML = `
                <div class="aspect-title">${section}</div>
                <div class="progress-count">0 / ${TOTAL} pertanyaan terjawab</div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width:0%; background:${color}"></div>
                </div>
            `;
    
            aspectList.appendChild(div);
        });
    }

    async function loadUserChats() {
        const res = await apiFetch(`/api/chat/user/${user_id}`);
        conversationList.innerHTML = "";

        res.data.array.forEach(chat => {
            const div = document.createElement("div");
            div.textContent = `Chat ${chat._id}`;
            div.onclick = () => loadChat(chat._id);
            conversationList.appendChild(div);
        });
    }

    async function loadChat(chatId) {
        const res = await apiFetch(`/chat/${chatId}`);
        chatWindow.innerHTML = "";
        currentChatId = chatId;

        res.data.items.forEach(item => {
            if (item.user_answer) addMessage(item.user_answer, "user");
            if (item.ai_response) addMessage(item.ai_response, "bot");
        });
        loadAspectProgress();
    }

    async function loadAspectProgress() {
        if (!currentChatId) {
            renderEmptyProgress();
            return;
        }
    
        const res = await apiFetch("/api/chat/simulate-aspect-progress", {
            method: "POST",
            body: JSON.stringify({
                section: window.currentSection || "Opening",
                group_id: window.currentGroupId || 0
            }),
        });
    
        aspectList.innerHTML = "";
    
        const progressMap = {};
        res.data.forEach(item => {
            progressMap[item.section] = item.percentage;
        });
    
        ALL_SECTIONS.forEach(section => {
            const percent = progressMap[section] || 0;
            const color = SECTION_COLORS[section] || "#4caf50";
    
            const div = document.createElement("div");
            div.className = "aspect-item";
    
            div.innerHTML = `
                <div class="aspect-title">${section}</div>
                <div class="progress-bar">
                    <div class="progress-fill"
                         style="width:${percent}%; background:${color}"></div>
                </div>
                <div class="progress-text">${percent}%</div>
            `;
    
            aspectList.appendChild(div);
        });
    }
    

    newChatBtn.addEventListener("click", async () => {
        const res = await apiFetch(`/api/chat/start-new-chat`, {
            method: "POST",
            body: JSON.stringify({user_id}),
        });
    
        currentChatId = res.data.chat_id;
    
        window.currentGroupId = 1;
        window.currentSection = "Opening";
    
        chatWindow.innerHTML = "";
    
        addMessage("Halo Rizki Pratama, terima kasih sudah meluangkan waktu untuk berbincang hari ini. Aku ingin memulai dengan beberapa pertanyaan ringan tentang bagaimana perasaanmu belakangan ini. Biasanya kamu lebih nyaman dipanggil siapa?", "bot");
        
        renderEmptyProgress();  
    });

    chatForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        if (!currentChatId) {
            alert("Silakan mulai percakapan baru terlebih dahulu.");
            return;
        }

        const userText = messageInput.value.trim();
        if (!userText) return;

        addMessage(userText, "user");
        messageInput.value = "";

        const sim = await apiFetch("/api/chat/simulate-conversation", {
            method: "POST",
            body: JSON.stringify({
                group_id: window.currentGroupId || 1,
                section: window.currentSection || "Opening"
            }),
        });
        
        const simData = sim.data;
        
        window.currentGroupId = simData.next_group_id;
        window.currentSection = simData.next_section;
        
        addMessage(simData.assistant_content, "bot");
        loadAspectProgress();
    });
    

    renderEmptyProgress(); 
});


