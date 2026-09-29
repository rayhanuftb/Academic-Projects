const API = '/api';

document.addEventListener('DOMContentLoaded', () => {
    loadStats();
    loadStudents();
    loadRooms();
    loadPayments();
    loadMaintenance();
});

function switchTab(tab) {
    document.querySelectorAll('.tab-panel').forEach(p => p.classList.add('hidden'));
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.getElementById(`tab-${tab}`)?.classList.remove('hidden');
    event.target.classList.add('active');
}

function openModal(id) { document.getElementById(id)?.classList.remove('hidden'); }
function closeModal(id) { document.getElementById(id)?.classList.add('hidden'); }

async function loadStats() {
    try {
        const res = await fetch(`${API}/stats`);
        const data = await res.json();
        document.getElementById('stat-students').textContent = data.totalStudents;
        document.getElementById('stat-rooms').textContent = data.totalRooms;
        document.getElementById('stat-occupied').textContent = data.occupiedBeds;
        document.getElementById('stat-available').textContent = data.availableBeds;
    } catch (_) {}
}

async function loadStudents() {
    try {
        const res = await fetch(`${API}/students`);
        const data = await res.json();
        const tbody = document.getElementById('table-students-body');
        const selStudent = document.getElementById('ar-student');
        
        tbody.innerHTML = (data.students || []).map(s => `
            <tr>
                <td><strong>${s.student_id}</strong></td>
                <td>${s.name}</td>
                <td>${s.department}</td>
                <td>${s.room_number ? `${s.block_name} - Room ${s.room_number}` : '<span class="badge badge-warning">Unallocated</span>'}</td>
                <td><span class="badge ${s.allocation_status === 'Active' ? 'badge-success' : 'badge-warning'}">${s.allocation_status || 'Pending'}</span></td>
            </tr>
        `).join('');

        if (selStudent) {
            selStudent.innerHTML = (data.students || []).map(s => `<option value="${s.id}">${s.student_id} - ${s.name}</option>`).join('');
        }
    } catch (_) {}
}

async function loadRooms() {
    try {
        const res = await fetch(`${API}/rooms`);
        const data = await res.json();
        const tbody = document.getElementById('table-rooms-body');
        const selRoom = document.getElementById('ar-room');

        tbody.innerHTML = (data.rooms || []).map(r => {
            const avail = r.capacity - r.occupied_count;
            return `
                <tr>
                    <td><strong>${r.block_name}</strong></td>
                    <td>Room ${r.room_number}</td>
                    <td>Floor ${r.floor_number}</td>
                    <td>${r.capacity} Beds</td>
                    <td>${r.occupied_count} Students</td>
                    <td><span class="badge ${avail > 0 ? 'badge-success' : 'badge-warning'}">${avail > 0 ? `${avail} Beds Free` : 'Full'}</span></td>
                </tr>
            `;
        }).join('');

        if (selRoom) {
            selRoom.innerHTML = (data.rooms || []).filter(r => (r.capacity - r.occupied_count) > 0).map(r => `<option value="${r.id}">${r.block_name} - Room ${r.room_number} (${r.capacity - r.occupied_count} Free)</option>`).join('');
        }
    } catch (_) {}
}

async function loadPayments() {
    try {
        const res = await fetch(`${API}/payments`);
        const data = await res.json();
        const tbody = document.getElementById('table-payments-body');
        tbody.innerHTML = (data.payments || []).map(p => `
            <tr>
                <td><strong>${p.student_name}</strong></td>
                <td>${p.student_code}</td>
                <td>${p.month_year}</td>
                <td>৳${p.amount.toFixed(2)}</td>
                <td><span class="badge badge-success">${p.payment_status}</span></td>
                <td>${p.paid_at}</td>
            </tr>
        `).join('');
    } catch (_) {}
}

async function loadMaintenance() {
    try {
        const res = await fetch(`${API}/maintenance`);
        const data = await res.json();
        const tbody = document.getElementById('table-maintenance-body');
        tbody.innerHTML = (data.issues || []).map(m => `
            <tr>
                <td>${m.block_name} - Rm ${m.room_number}</td>
                <td>${m.issue_description}</td>
                <td><span class="badge badge-warning">${m.priority}</span></td>
                <td>${m.status}</td>
                <td>${m.reported_at}</td>
            </tr>
        `).join('');
    } catch (_) {}
}

async function handleAddStudent(e) {
    e.preventDefault();
    const student_id = document.getElementById('ms-id').value;
    const name = document.getElementById('ms-name').value;
    const email = document.getElementById('ms-email').value;
    const department = document.getElementById('ms-dept').value;

    await fetch(`${API}/students`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ student_id, name, email, department })
    });
    closeModal('modal-add-student');
    loadStudents();
    loadStats();
}

async function handleAllocateRoom(e) {
    e.preventDefault();
    const student_id = parseInt(document.getElementById('ar-student').value);
    const room_id = parseInt(document.getElementById('ar-room').value);

    await fetch(`${API}/allocations`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ student_id, room_id })
    });
    closeModal('modal-allocate-room');
    loadStudents();
    loadRooms();
    loadStats();
}
