let currentViewDate = new Date(2026, 4, 1); // Default: May 2026

const englishMonths = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
const englishWeekdays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];

// =========================================================================
// 1. API SERVICE ENDPOINTS
// =========================================================================

/**
 * Fetches lesson data for a specific month from the backend API.
 */
async function fetchMonthLessonsFromAPI(year, month) {
    try {
        // Python tarafına (aylar 1-12 arası olduğu için) month + 1 gönderiyoruz
        const response = await fetch(`/api/lessons?year=${year}&month=${month + 1}`);
        if (!response.ok) return [];
        return await response.json();
    } catch (error) {
        console.error("Error fetching monthly lessons from API:", error);
        return [];
    }
}

/**
 * Fetches the 24-hour schedule details for a selected day from the API.
 */
async function fetchDayScheduleFromAPI(dateStr) {
    try {
        const response = await fetch(`/api/schedule/${dateStr}`);
        if (!response.ok) return [];
        return await response.json();
    } catch (error) {
        console.error("Error fetching daily schedule from API:", error);
        return [];
    }
}

/**
 * Sends a POST request to API to save a new lesson for a specific hour.
 */
async function saveLessonToAPI(dateStr, timeSlot) {
    try {
        const response = await fetch('/api/lessons/add', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ date: dateStr, time: timeSlot })
        });

        if (response.ok) {
            renderCalendar(); // Takvimi yenile (noktalar güncellensin)

            // Modal içindeki güncel saat listesini yenile
            const dateObj = new Date(dateStr);
            openModal(dateObj.getDate(), dateObj.getMonth(), dateObj.getFullYear());
        }
    } catch (error) {
        console.error("Error saving lesson to API:", error);
    }
}


// =========================================================================
// 2. INTERFACE, DOM OPERATIONS & DYNAMIC FOOTER
// =========================================================================

/**
 * Dynamically updates the footer with today's real date in English format.
 */
function setDynamicFooterToday() {
    const footerElement = document.getElementById('footerTodayText');
    if (footerElement) {
        const today = new Date();
        const dayName = englishWeekdays[today.getDay()];
        const monthName = englishMonths[today.getMonth()];
        const dateNum = today.getDate();
        const year = today.getFullYear();

        footerElement.innerText = `${dayName}, ${monthName} ${dateNum}, ${year}`;
        footerElement.setAttribute('datetime', today.toISOString().split('T')[0]);
    }
}

async function renderCalendar() {
    const daysGrid = document.getElementById('calendarDays');
    const label = document.getElementById('currentMonthLabel');
    daysGrid.innerHTML = "";

    const year = currentViewDate.getFullYear();
    const month = currentViewDate.getMonth();
    label.innerText = `${englishMonths[month]} ${year}`;

    renderMonthTabs(month, year);

    const monthLessons = await fetchMonthLessonsFromAPI(year, month);

    let firstDayIndex = new Date(year, month, 1).getDay();
    firstDayIndex = firstDayIndex === 0 ? 6 : firstDayIndex - 1;

    const totalDaysInMonth = new Date(year, month + 1, 0).getDate();

    for (let i = 0; i < firstDayIndex; i++) {
        const emptyBox = document.createElement('div');
        emptyBox.className = 'day-box empty';
        daysGrid.appendChild(emptyBox);
    }

    const todayObj = new Date();

    for (let dayNum = 1; dayNum <= totalDaysInMonth; dayNum++) {
        const dayDiv = document.createElement('div');
        dayDiv.className = 'day-box';

        if (dayNum === todayObj.getDate() && month === todayObj.getMonth() && year === todayObj.getFullYear()) {
            dayDiv.classList.add('today');
        }

        const hasLesson = monthLessons.some(item => item.day === dayNum && item.hasLesson);
        let lessonIndicator = hasLesson ? `<span class="lesson-dot" style="width:6px; height:6px; background:#1461f2; border-radius:50%; display:block; margin-top:5px;"></span>` : '';

        dayDiv.innerHTML = `
            <strong>${dayNum}</strong>
            <span class="plus">+</span>
            ${lessonIndicator}
        `;

        dayDiv.onclick = () => openModal(dayNum, month, year);
        daysGrid.appendChild(dayDiv);
    }
}

function renderMonthTabs(activeMonthIndex, currentYear) {
    const tabsContainer = document.getElementById('monthTabsContainer');
    tabsContainer.innerHTML = "";

    for (let i = 4; i <= 8; i++) { // May to September
        const tabBtn = document.createElement('button');
        tabBtn.className = `tab ${i === activeMonthIndex ? 'active' : ''}`;
        tabBtn.innerText = `${englishMonths[i]} ${currentYear}`;
        tabBtn.onclick = () => {
            currentViewDate.setMonth(i);
            renderCalendar();
        };
        tabsContainer.appendChild(tabBtn);
    }
}

async function openModal(day, month, year) {
    const formattedDate = `${year}-${(month + 1).toString().padStart(2, '0')}-${day.toString().padStart(2, '0')}`;
    const targetDate = new Date(year, month, day);

    document.getElementById('modalTitle').innerText = `${englishMonths[month]} ${day}, ${year} - ${englishWeekdays[targetDate.getDay()]}`;
    const hourListContainer = document.getElementById('hourList');
    hourListContainer.innerHTML = "";

    const daySchedule = await fetchDayScheduleFromAPI(formattedDate);

    for (let hour = 0; hour < 24; hour++) {
        const row = document.createElement('div');
        row.className = 'hour-row-item';

        const startTime = hour.toString().padStart(2, '0') + ":00";
        const endTime = (hour + 1).toString().padStart(2, '0') + ":00";

        const hourData = daySchedule.find(item => item.hour === hour);
        const isFilled = hourData ? hourData.isFilled : false;
        const scheduleTitle = hourData ? hourData.title : "Empty";

        row.innerHTML = `
            <div class="hour-left-block">
                <div class="hour-time-range">${startTime}<br>${endTime}</div>
                <div class="hour-status-label" style="${isFilled ? 'color: #1461f2; font-weight: 600;' : ''}">
                    ${scheduleTitle}
                </div>
            </div>
            ${!isFilled ? `
                <button class="inline-add-btn" onclick="saveLessonToAPI('${formattedDate}', '${startTime}')">
                    <span>+</span> Add Lesson
                </button>
            ` : ''}
        `;
        hourListContainer.appendChild(row);
    }

    document.getElementById('dayModal').style.display = 'flex';
}

function closeModal() {
    document.getElementById('dayModal').style.display = 'none';
}

document.getElementById('prevBtn').onclick = () => {
    currentViewDate.setMonth(currentViewDate.getMonth() - 1);
    renderCalendar();
};
document.getElementById('nextBtn').onclick = () => {
    currentViewDate.setMonth(currentViewDate.getMonth() + 1);
    renderCalendar();
};

// Initial App Launches
renderCalendar();
setDynamicFooterToday(); // Dynamically outputs current date on page load


// =========================================================================
// 3. AI CHATBOX ENTEGRASYONU
// =========================================================================

const aiInput = document.getElementById('aiInput');
const chatBox = document.getElementById('chatBox');
const sendBtn = document.querySelector('.icon-send-btn');

async function sendChatMessage() {
    const message = aiInput.value.trim();
    if (!message) return;

    appendMessage(message, 'user');
    aiInput.value = '';

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: message })
        });

        if (response.ok) {
            const data = await response.json();
            appendMessage(data.response, 'bot'); // Yapay zekanın cevabını ekrana ekle
        } else {
            appendMessage("Üzgünüm, API'ye ulaşılamadı veya oturum süresi doldu.", 'bot');
        }
    } catch (error) {
        console.error("Chat Error:", error);
        appendMessage("Bağlantı hatası oluştu.", 'bot');
    }
}

function appendMessage(text, sender) {
    const rowDiv = document.createElement('div');
    rowDiv.className = `chat-message-row ${sender}-row`;

    if (sender === 'user') {
        rowDiv.innerHTML = `
            <div class="bubble user"></div>
            <div class="message-action-tag">You</div>
        `;
        rowDiv.querySelector('.bubble').textContent = text;
    } else {
        rowDiv.innerHTML = `
            <div class="message-avatar">🤖</div>
            <div class="bubble bot"></div>
        `;
        rowDiv.querySelector('.bubble').textContent = text;
    }

    chatBox.appendChild(rowDiv);

    chatBox.scrollTop = chatBox.scrollHeight;
}

if (sendBtn) {
    sendBtn.addEventListener('click', sendChatMessage);
}

if (aiInput) {
    aiInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            sendChatMessage();
        }
    });



    // =========================================================================
// 4. UPLOAD SCREENSHOT FEATURE (DERS PROGRAMI YÜKLEME)
// =========================================================================

const uploadScheduleBtn = document.getElementById('uploadScheduleBtn');
const scheduleFileInput = document.getElementById('scheduleFileInput');
const uploadStatus = document.getElementById('uploadStatus');

if (uploadScheduleBtn && scheduleFileInput) {
    uploadScheduleBtn.addEventListener('click', () => {
        scheduleFileInput.click();
    });

    scheduleFileInput.addEventListener('change', async (event) => {
        const file = event.target.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append('schedule_image', file);

        uploadScheduleBtn.disabled = true;
        uploadStatus.innerText = "Yapay zeka programı inceliyor, lütfen bekleyin... ⏳";
        uploadStatus.style.color = "#1d63ed";

        try {
            const response = await fetch('/api/upload_schedule', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (response.ok && data.success) {
                uploadStatus.innerText = "✅ " + data.message;
                uploadStatus.style.color = "green";
                renderCalendar(); // Yeni dersler geldi, takvimi yenile
            } else {
                uploadStatus.innerText = "❌ Hata: " + (data.error || "Bilinmeyen bir hata oluştu.");
                uploadStatus.style.color = "red";
            }
        } catch (error) {
            console.error("Upload error:", error);
            uploadStatus.innerText = "❌ Sunucu ile iletişim kurulamadı.";
            uploadStatus.style.color = "red";
        } finally {
            // İşlem bitince butonu tekrar aktif et ve inputu temizle
            uploadScheduleBtn.disabled = false;
            scheduleFileInput.value = "";
        }
    });
}
}