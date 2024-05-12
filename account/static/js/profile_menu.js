$(document).ready(function() {
    // Показываем меню при клике на фото
    $('#profile-avatar-menu-btn').click(function() {
//        alert("Avatar clicked");

        $('#profile-menu').toggle();
    });

    // Скрываем меню при клике вне его области
    $(document).click(function(event) {
        if (!$(event.target).closest('#profile-avatar-menu-btn, #profile-menu').length && !$(event.target).is('#profile-avatar-menu-btn')) {
            $('#profile-menu').hide();
        }
    });
});