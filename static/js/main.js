// ─── MODAL HELPERS ───
function openModal(id) {
  document.getElementById(id).style.display = 'flex';
  document.body.style.overflow = 'hidden';
}

function closeModal(id) {
  document.getElementById(id).style.display = 'none';
  document.body.style.overflow = '';
}

// Close modal on overlay click
document.addEventListener('click', function(e) {
  if (e.target.classList.contains('modal-overlay')) {
    e.target.style.display = 'none';
    document.body.style.overflow = '';
  }
});

// Close on Escape
document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') {
    document.querySelectorAll('.modal-overlay').forEach(m => {
      m.style.display = 'none';
    });
    document.body.style.overflow = '';
  }
});

// ─── SIDEBAR TOGGLE (Mobile) ───
function toggleSidebar() {
  document.getElementById('sidebar').classList.toggle('open');
}

// ─── DELETE CONFIRM ───
function confirmDelete(label) {
  return confirm(`Apakah Anda yakin ingin menghapus ${label || 'data ini'}?\nTindakan ini tidak dapat dibatalkan.`);
}

// ─── AUTO DISMISS FLASH ───
setTimeout(function() {
  document.querySelectorAll('.flash').forEach(function(el) {
    el.style.opacity = '0';
    el.style.transition = 'opacity 0.5s';
    setTimeout(() => el.remove(), 500);
  });
}, 4000);

// ─── NUMBER FORMATTING DISPLAY ───
document.querySelectorAll('input[type="number"]').forEach(function(el) {
  el.addEventListener('input', function() {
    if (this.value < 0) this.value = 0;
  });
});
