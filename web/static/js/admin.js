document.addEventListener("DOMContentLoaded", () => {

    const aspects = [
        "Depresi","Amarah","Mania","Kecemasan","Somatik",
        "Kecenderungan Bunuh Diri","Psikosis","Gangguan Tidur","Gangguan Memori",
        "Disosiasi","Penggunaan Substansi","Pemikiran Berulang"
    ];

    function randomScores() {
        return aspects.reduce((a, b) => {
            a[b] = Math.floor(Math.random() * 101);
            return a;
        }, {});
    }

    function randomName() {
        const n = ["Alice","Budi","Citra","Dina","Eko","Farah","Gilang","Hana","Ivan","Joko"];
        return n[Math.floor(Math.random() * n.length)];
    }

    const users = Array.from({ length: 15 }, (_, i) => ({
        id: i + 1,
        name: randomName(),
        email: `user${i+1}@mail.com`,
        scores: randomScores()
    }));

    let currentUser = null;

    const list = document.querySelector(".conversation-list");
    const windowBox = document.querySelector(".chat-window");
    const title = document.querySelector(".chat-area h2");
    const search = document.getElementById("user-search");
    const downloadBtn = document.getElementById("download-excel-btn");

    function renderUsers(arr) {
        list.innerHTML = "";

        arr.forEach(u => {
            const item = document.createElement("div");
            item.className = "conversation-item";
            item.innerHTML = `<strong>${u.name}</strong> — ${u.email}`;
            item.onclick = () => showUser(u);
            list.appendChild(item);
        });
    }

    function showUser(user) {
        currentUser = user;
        title.textContent = `Hasil — ${user.name} (${user.email})`;
        windowBox.innerHTML = "";

        aspects.forEach(a => {
            const v = user.scores[a];

            const box = document.createElement("div");
            box.className = "aspect-item";
            box.innerHTML = `
                <div class="aspect-title">${a}</div>
                <div class="progress-bar">
                    <div class="progress-fill"></div>
                </div>
                <div class="progress-text">${v}%</div>
            `;

            windowBox.appendChild(box);

            const fill = box.querySelector(".progress-fill");
            setTimeout(() => fill.style.width = v + "%", 30);
        });
    }

    search.addEventListener("input", e => {
        const val = e.target.value.toLowerCase();
        renderUsers(
            users.filter(u =>
                u.name.toLowerCase().includes(val) ||
                u.email.toLowerCase().includes(val)
            )
        );
    });

    downloadBtn.addEventListener("click", () => {
        if (!currentUser) return;

        const data = aspects.map(a => ({
            Aspect: a,
            Score: currentUser.scores[a]
        }));

        const ws = XLSX.utils.json_to_sheet(data);
        const wb = XLSX.utils.book_new();

        XLSX.utils.book_append_sheet(wb, ws, "Report");
        XLSX.writeFile(wb, `${currentUser.name}_report.xlsx`);
    });

    renderUsers(users);
    showUser(users[0]);

});
