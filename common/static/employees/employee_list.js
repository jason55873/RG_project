function getCsrfToken() {
  return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}
function getCurrentLang() {
  return document.querySelector('meta[name="current-lang"]').getAttribute('content');
}

const csrfToken = getCsrfToken();
const lang = getCurrentLang();

document.addEventListener('DOMContentLoaded', function() {
  fetch(`/${lang}/common/employees/list/`)
    .then(response => response.json())
    .then(data => {
      const tbody = document.querySelector('#employee-table tbody');
      tbody.innerHTML = '';
      data.forEach(emp => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td>${emp.employee_no}</td>
          <td>${emp.username || ''}</td>
          <td>${emp.email || ''}</td>
          <td>${emp.employee_name || ''}</td>
          <td>${emp.title || ''}</td>
          <td>${emp.department_id || ''}</td>
          <td>
            <a href="/${lang}/common/employees/${emp.id}/update/" class="btn btn-sm btn-primary">編輯</a>
            <button class="btn btn-sm btn-danger delete-btn" data-id="${emp.id}">刪除</button>
          </td>
        `;
        tbody.appendChild(tr);
      });

      tbody.addEventListener('click', function(e) {
        if (e.target.classList.contains('delete-btn')) {
          const id = e.target.getAttribute('data-id');
          if (!confirm('確定要刪除？')) return;
          fetch(`/api/employees/${id}/`, {
            method: 'DELETE',
            headers: {'X-CSRFToken': csrfToken}
          })
          .then(response => {
            if (response.status === 204) {
              location.reload();
            } else {
              alert('刪除失敗');
            }
          });
        }
      });
    })
    .catch(err => {
      alert('載入員工資料失敗');
      console.error(err);
    });
});

function deleteEmployee(id) {
  if (!confirm('確定要刪除？')) return;
  fetch(`/api/employees/${id}/`, {
    method: 'DELETE',
    headers: {'X-CSRFToken': csrfToken}
  })
  .then(response => {
    if (response.status === 204) {
      location.reload();
    } else {
      alert('刪除失敗');
    }
  });
}