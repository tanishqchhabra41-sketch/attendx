let attendanceData = [];


async function addStudent() {

    const roll = document.getElementById('studentRoll').value;

    const name = document.getElementById('studentName').value;

    const message = document.getElementById('message');


    if (!roll || !name) {

        message.innerHTML = "Please Fill All Fields";

        message.style.color = "#ef4444";

        return;
    }


    const response = await fetch('/add_student', {

        method: 'POST',

        headers: {
            'Content-Type': 'application/json'
        },

        body: JSON.stringify({
            roll,
            name
        })
    });


    const data = await response.json();


    if (data.success) {

        message.innerHTML = data.message;

        message.style.color = "#22c55e";

        document.getElementById('studentRoll').value = '';

        document.getElementById('studentName').value = '';

        loadStudents();

        loadRecords();

    } else {

        message.innerHTML = data.message;

        message.style.color = "#ef4444";
    }
}



async function loadStudents() {

    const response = await fetch('/get_students');

    const students = await response.json();

    const container = document.getElementById('studentAttendanceList');

    container.innerHTML = '';

    attendanceData = [];


    students.forEach(student => {

        attendanceData.push({

            roll: student.roll,

            name: student.name,

            status: 'P'
        });


        const row = document.createElement('div');

        row.className = 'student-row';


        row.innerHTML = `

            <div class="student-info">

                <h3>${student.name}</h3>

                <p>Roll No : ${student.roll}</p>

            </div>


            <div class="attendance-buttons">

                <button
                    class="present-btn active-present"
                    onclick="markAttendance('${student.roll}','P',this)">
                    P
                </button>

                <button
                    class="absent-btn"
                    onclick="markAttendance('${student.roll}','A',this)">
                    A
                </button>

            </div>
        `;

        container.appendChild(row);
    });
}



function markAttendance(roll, status, button) {

    const parent = button.parentElement;

    const buttons = parent.querySelectorAll('button');

    buttons.forEach(btn => {

        btn.classList.remove('active-present');

        btn.classList.remove('active-absent');
    });


    if (status === 'P') {

        button.classList.add('active-present');

    } else {

        button.classList.add('active-absent');
    }


    attendanceData = attendanceData.map(student => {

        if (student.roll === roll) {

            student.status = status;
        }

        return student;
    });
}



async function saveAttendance() {

    const message = document.getElementById('message');


    const response = await fetch('/add_attendance', {

        method: 'POST',

        headers: {
            'Content-Type': 'application/json'
        },

        body: JSON.stringify({
            attendance: attendanceData
        })
    });


    const data = await response.json();


    if (data.success) {

        message.innerHTML = data.message;

        message.style.color = "#22c55e";

        loadRecords();

    } else {

        message.innerHTML = data.message;

        message.style.color = "#ef4444";
    }
}



async function loadRecords() {

    const response = await fetch('/view_records');

    const records = await response.json();

    const table = document.getElementById('recordsTable');

    table.innerHTML = '';


    records.forEach(record => {

        let percentageClass = 'high';


        if (record.percentage < 75) {

            percentageClass = 'low';

        } else if (record.percentage < 90) {

            percentageClass = 'medium';
        }


        const row = `

            <tr>

                <td>${record.roll}</td>

                <td>${record.name}</td>

                <td class="${percentageClass}">
                    ${record.percentage}%
                </td>

            </tr>
        `;

        table.innerHTML += row;
    });
}


window.onload = () => {

    loadStudents();

    loadRecords();
};