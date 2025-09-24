document.addEventListener('DOMContentLoaded', function() {
  const table = document.querySelector('#employee-table');
  const ajaxUrl = table.getAttribute('data-ajax-url');
  const csrfToken = window.csrfToken;

  fetch(ajaxUrl)
    .then(response => response.json())
    .then(data => {
      const tbody = document.querySelector('#employee-table tbody');
      tbody.innerHTML = '';
      data.forEach(emp => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td>${emp.employee_id || ''}</td>
          <td>${emp.name_chinese || ''}</td>
          <td>${emp.name_english || ''}</td>
          <td>${emp['department__name'] || ''}</td>
          <td>${emp.position || ''}</td>
          <td>${emp['user__username'] || ''}</td>
          <td>
            <a href="/employee/update/${emp.id}/" class="btn btn-sm btn-primary">編輯</a>
            <form method="post" action="/employee/delete/${emp.id}/" class="d-inline delete-form">
              <input type="hidden" name="csrfmiddlewaretoken" value="{{ csrf_token }}">
              <button type="submit" class="btn btn-sm btn-danger">刪除</button>
            </form>
          </td>
        `;
        tbody.appendChild(tr);
      });

      // 綁定刪除確認
      document.querySelectorAll('.delete-form').forEach(form => {
        form.addEventListener('submit', function(e) {
          if (!confirm('你確定要刪除此人員嗎？')) {
            e.preventDefault();
          }
        });
      });
    });
});