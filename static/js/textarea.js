document.querySelector('.list_header_itemInput').keyup(function () {
    this.style.height = "1px";
    this.style.height = (this.scrollHeight + 1) + "px";
});