const API_URL = "http://127.0.0.1:5000/data";

// Fetch and display data
async function fetchData() {
    const response = await fetch(API_URL);
    const data = await response.json();
    
    const dataList = document.getElementById("data-list");
    dataList.innerHTML = "";

    data.forEach(item => {
        const li = document.createElement("li");
        li.innerHTML = `${item.name}: ${item.value} 
            <button class="delete-btn" onclick="deleteData(${item.id})">Delete</button>`;
        dataList.appendChild(li);
    });
}

// Add new data
async function addData() {
    const name = document.getElementById("name").value;
    const value = document.getElementById("value").value;

    if (!name || !value) {
        alert("Please enter both name and value!");
        return;
    }

    await fetch(API_URL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ name, value })
    });

    document.getElementById("name").value = "";
    document.getElementById("value").value = "";

    fetchData();
}

// Delete data
async function deleteData(id) {
    await fetch(`${API_URL}/${id}`, { method: "DELETE" });
    fetchData();
}

// Load data when the page loads
window.onload = fetchData;
