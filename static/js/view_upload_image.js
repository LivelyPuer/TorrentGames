function readURL(input) {

    if (input.files && input.files[0] && document.querySelector("#image_url").value === "") {
        var reader = new FileReader();

        reader.onload = function (e) {
            document.querySelector('#image').src = e.target.result;
        };

        reader.readAsDataURL(input.files[0]);
    }
}

function readURLtext(input) {
    console.log(input.value.toString());
    document.querySelector('#image').src = input.value;
}

