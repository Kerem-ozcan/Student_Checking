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
        // API_CONNECTION: const response = await fetch(`/api/lessons?year=${year}&month=${month + 1}`);
        // return await response.json();
        
        return []; // Default empty data
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
        // API_CONNECTION: const response = await fetch(`/api/schedule/${dateStr}`);
        // return await response.json();
        
        return []; // Default empty data
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
        // API_CONNECTION: 
        // const response = await fetch('/api/lessons/add', {
        //     method: 'POST',
        //     headers: { 'Content-Type': 'application/json' },
        //     body: JSON.stringify({ date: dateStr, time: timeSlot })
        // });
        // if (response.ok) { 
        //     renderCalendar(); 
        //     openModal(new Date(dateStr).getDate(), new Date(dateStr).getMonth(), new Date(dateStr).getFullYear());
        // }
        
        console.log(`Add Lesson Request -> Date: ${dateStr}, Time: ${timeSlot}`);
    } catch (error) {
        console.error("Error saving lesson to API:", error);
    }
}


// =========================================================================
// 2. INTERFACE, DOM OPERATIONS & DYNAMIC FOOTER
// =========================================================================

/**
 * Dynamically updates the footer with today's real date in English format.
 * Example: "Today: Wednesday, May 6, 2026"
 */
function setDynamicFooterToday() {
    const footerElement = document.getElementById('footerTodayText');
    if (footerElement) {
        const today = new Date();
        const dayName = englishWeekdays[today.getDay()];
        const monthName = englishMonths[today.getMonth()];
        const dateNum = today.getDate();
        const year = today.getFullYear();
        
        // Output format: Wednesday, May 6, 2026
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

    // Fetch this month's lessons from API
    const monthLessons = await fetchMonthLessonsFromAPI(year, month);

    let firstDayIndex = new Date(year, month, 1).getDay();
    firstDayIndex = firstDayIndex === 0 ? 6 : firstDayIndex - 1; 

    const totalDaysInMonth = new Date(year, month + 1, 0).getDate();

    // Empty grid cells for day offset
    for (let i = 0; i < firstDayIndex; i++) {
        const emptyBox = document.createElement('div');
        emptyBox.className = 'day-box empty';
        daysGrid.appendChild(emptyBox);
    }

    // Days list
    for (let dayNum = 1; dayNum <= totalDaysInMonth; dayNum++) {
        const dayDiv = document.createElement('div');
        dayDiv.className = 'day-box';
        
        // Highlight Today (System current date is May 6, 2026)
        if (dayNum === 6 && month === 4 && year === 2026) {
            dayDiv.classList.add('today');
        }
        
        // Add indicator if there is a lesson from API
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
    
    // Fetch schedule data for selected day
    const daySchedule = await fetchDayScheduleFromAPI(formattedDate);
    
    for (let hour = 0; hour < 24; hour++) {
        const row = document.createElement('div');
        row.className = 'hour-row-item';
        
        const startTime = hour.toString().padStart(2, '0') + ":00";
        const endTime = (hour + 1).toString().padStart(2, '0') + ":00";
        
        const hourData = daySchedule.find(item => item.hour === hour);
        const isFilled = hourData ? hourData.isFilled : false;
        const scheduleTitle = hourData ? hourData.title : "Empty"; // Translated status to English

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

// Navigation Arrow Clicks
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