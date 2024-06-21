document.addEventListener("DOMContentLoaded", () => {
    const themeToggle = document.getElementById("theme-toggle");
    const body = document.body;
    const header = document.querySelector("header");
    const taskBoard = document.getElementById("task-board");
    const addTaskCard = document.getElementById("add-task");


    fetch('/current-user')
        .then(response => response.json())
        .then(user => {
            currentUserId = user.id;
                //Upload Theme
                fetch(`/get-theme`)
                .then(response => response.json())
                .then(data => {
                    const theme = data.theme;
                    if (theme === 'dark') {
                        body.classList.add("dark");
                        header.classList.add("dark");
                        themeToggle.textContent = "🙂";
                    } else {
                        body.classList.remove("dark");
                        header.classList.remove("dark");
                        themeToggle.textContent = "😴";
                    }
                });

            loadTasks();
        });


    
    fetch('/get-tasks')
        .then(response => response.json())
        .then(tasks => {
            tasks.forEach(task => {
                const newTaskCard = createTaskCard(task.id, task.title, task.description, task.deadline, task.user_id, true);
                taskBoard.insertBefore(newTaskCard, addTaskCard);
            });
        });

    addTaskCard.addEventListener("click", () => {
        const today = new Date().toISOString().split('T')[0];
        const newTaskCard = createTaskCard(null, "", "", today, currentUserId, false); // Replace 1 with appropriate user_id
        taskBoard.insertBefore(newTaskCard, addTaskCard);
    });

    function createTaskCard(taskId, title, description, deadline, user_id, isSaved) {
        const newTaskCard = document.createElement("div");
        newTaskCard.classList.add("task-card");
        newTaskCard.setAttribute("data-task-id", taskId); // Store taskId in the element
        newTaskCard.innerHTML = `
            <div class="task-title">Title: <input type="text" placeholder="Enter title" class="editable" value="${title}" ${isSaved ? 'readonly' : ''}></div>
            <div class="task-content">Description: <textarea placeholder="Enter description" class="editable" rows="2" ${isSaved ? 'readonly' : ''}>${description}</textarea></div>
            <input type="date" class="task-deadline" value="${deadline}" ${isSaved ? 'readonly' : ''}>
            <div class="task-actions">
                <div class="icon save-icon" style="display: ${isSaved ? 'none' : 'inline-block'};">save</div>
                <div class="icon delete-icon">🗑️</div>
                <div class="icon edit-icon" style="display: ${isSaved ? 'inline-block' : 'none'};">✏️</div>
                <div class="icon check-icon" style="display: ${isSaved ? 'inline-block' : 'none'};">✅</div>
            </div>
        `;

        const saveIcon = newTaskCard.querySelector(".save-icon");
        const deleteIcon = newTaskCard.querySelector(".delete-icon");
        const checkIcon = newTaskCard.querySelector(".check-icon");
        const editIcon = newTaskCard.querySelector(".edit-icon");
        const titleEditable = newTaskCard.querySelector(".task-title .editable");
        const descEditable = newTaskCard.querySelector(".task-content .editable");

        titleEditable.focus();

        saveIcon.addEventListener("click", () => {
            const title = titleEditable.value;
            const description = descEditable.value;
            const deadline = newTaskCard.querySelector(".task-deadline").value;

            const taskData = { title, description, deadline, user_id };

            if (taskId) {
                fetch(`/update-task/${taskId}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(taskData)
                }).then(response => response.json())
                  .then(data => {
                      console.log(data); // Log server response
                      titleEditable.setAttribute("readonly", "true");
                      descEditable.setAttribute("readonly", "true");
                      newTaskCard.querySelector(".task-deadline").setAttribute("readonly", "true");
                      saveIcon.style.display = "none";
                      editIcon.style.display = "inline-block";
                      checkIcon.style.display = "inline-block";
                  });
            } else {
                fetch('/save-task', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(taskData)
                }).then(response => response.json())
                  .then(data => {
                      console.log(data); // Log server response
                      titleEditable.setAttribute("readonly", "true");
                      descEditable.setAttribute("readonly", "true");
                      newTaskCard.querySelector(".task-deadline").setAttribute("readonly", "true");
                      saveIcon.style.display = "none";
                      editIcon.style.display = "inline-block";
                      checkIcon.style.display = "inline-block";
                      taskId = data.task_id; // Update taskId after save
                      newTaskCard.setAttribute("data-task-id", taskId); // Store taskId in the element
                  });
            }
        });

        deleteIcon.addEventListener("click", () => {
            if (taskId) {
                fetch(`/delete-task/${taskId}`, {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                }).then(response => response.json())
                  .then(data => {
                      console.log(data); // Log server response
                      newTaskCard.remove();
                  });
            } else {
                newTaskCard.remove();
            }
        });

        checkIcon.addEventListener("click", () => {
            if (taskId) {
                fetch(`/mark-task-done/${taskId}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                }).then(response => response.json())
                  .then(data => {
                      console.log(data); // Log server response
                      newTaskCard.remove();
                  });
            } else {
                newTaskCard.remove();
            }
        });

        editIcon.addEventListener("click", () => {
            titleEditable.removeAttribute("readonly");
            descEditable.removeAttribute("readonly");
            newTaskCard.querySelector(".task-deadline").removeAttribute("readonly");
            titleEditable.focus();
            saveIcon.style.display = "inline-block";
            editIcon.style.display = "none";
            checkIcon.style.display = "none";
        });

        titleEditable.addEventListener("input", () => {
            if (/[\u0600-\u06FF]/.test(titleEditable.value)) {
                titleEditable.setAttribute("lang", "fa");
            } else {
                titleEditable.removeAttribute("lang");
            }
        });

        descEditable.addEventListener("input", () => {
            if (/[\u0600-\u06FF]/.test(descEditable.value)) {
                descEditable.setAttribute("lang", "fa");
            } else {
                descEditable.removeAttribute("lang");
            }
        });

        return newTaskCard;
    }

    themeToggle.addEventListener("click", () => {
        body.classList.toggle("dark");
        header.classList.toggle("dark");
        const theme = body.classList.contains("dark") ? 'dark' : 'light';
        themeToggle.textContent = body.classList.contains("dark") ? "🙂" : "😴";
        // Send Theme
        fetch('/update-theme', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ theme: theme })
        }).then(response => response.json())
          .then(data => {
              console.log(data); // Log server response
          });
    });
});
