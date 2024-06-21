document.addEventListener("DOMContentLoaded", function() {
  // Получаем контейнер для звезд
  var starContainer = document.getElementById('particles-js');

  // Создаем и добавляем звезды в контейнер
  for (var i = 0; i < 80; i++) {
    var star = document.createElement('div');
    star.className = 'star';
    star.style.left = Math.random() * 100 + 'vw'; // случайное расположение по горизонтали
    star.style.top = Math.random() * 100 + 'vh'; // случайное расположение по вертикали
    star.style.animationDuration = Math.random() * 3 + 1 + 's'; // случайная продолжительность анимации (от 1 до 4 секунд)
    starContainer.appendChild(star);
  }
});
