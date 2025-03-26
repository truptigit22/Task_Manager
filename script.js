const API_URL = '/tasks';

// Handle form submission
document.getElementById('taskForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const taskData = {
        title: document.getElementById('title').value,
        description: document.getElementById('description').value,
        deadline: document.getElementById('deadline').value,
        time: document.getElementById('time').value,
        priority: document.getElementById('priority').value
    };

    await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(taskData)
    });

    e.target.reset();
    fetchTasks();
});

// Fetch tasks
async function fetchTasks() {
    const response = await fetch(API_URL);
    const tasks = await response.json();
    const taskList = document.getElementById('taskList');
    taskList.innerHTML = '';

    tasks.forEach(task => {
        const li = document.createElement('li');
        li.textContent = task.title;
        li.onclick = () => showDetails(task);
        
    const deleteBtn = document.createElement('button');
    deleteBtn.textContent = 'Delete';
    deleteBtn.classList.add('delete-btn'); // Apply the red button style
    deleteBtn.onclick = async (e) => {
    e.stopPropagation(); // Prevent triggering task details when clicking delete
    await fetch(`${API_URL}/${task.id}`, { method: 'DELETE' });
    fetchTasks();
    document.getElementById('taskDetails').classList.add('hidden'); // Hide details after delete
    };
        li.appendChild(deleteBtn);
        taskList.appendChild(li);
    });
}

// Show task details
function showDetails(task) {
    document.getElementById('taskTitle').textContent = task.title;
    document.getElementById('taskDescription').textContent = task.description;
    document.getElementById('taskdeadline').textContent = task.deadline;
    document.getElementById('tasktime').textContent = task.time;
    document.getElementById('taskpriority').textContent = task.priority;
    document.getElementById('taskDetails').classList.remove('hidden');
}

// Close task details
function closetaskDetails() {
    document.getElementById('taskDetails').classList.add('hidden'); // Hide details
}

// Load tasks on page load
fetchTasks();
