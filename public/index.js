$(document).ready(function () {
    $(".form__btn").on("click", function () {
        let isValid = $(".sentiment__input").prop("validity");
        if (isValid.valid) {
            $(".form__loading").css("display", "block");
        }
    });
});