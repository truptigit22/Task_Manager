const API_URL = 'http://127.0.0.1:5000/tasks';

// Fetch and display tasks
async function fetchTasks() {
    const response = await fetch(API_URL);
    const tasks = await response.json();

    const taskList = document.getElementById('taskList');
    taskList.innerHTML = '';

    tasks.forEach(task => {
        const li = document.createElement('li');
        li.innerHTML = `
            ${task.title} (${task.priority}) - ${task.deadline} ${task.time}
            <button class="delete" onclick="deleteTask(${task.id})">Delete</button>
        `;
        taskList.appendChild(li);
    });
}

// Add a new task
document.getElementById('taskForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const newTask = {
        title: document.getElementById('title').value,
        description: document.getElementById('description').value,
        deadline: document.getElementById('deadline').value,
        time: document.getElementById('time').value,
        priority: document.getElementById('priority').value
    };

    await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newTask)
    });

    fetchTasks(); // Refresh list
    e.target.reset();
});

// Delete a task
async function deleteTask(id) {
    await fetch(`${API_URL}/${id}`, { method: 'DELETE' });
    fetchTasks();
}

// Load tasks on page load
fetchTasks();
