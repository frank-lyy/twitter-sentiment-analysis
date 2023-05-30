function autoResize(element) {
    element.parentElement.style.width = element.value.length + 'ch';
    console.log(element.parentElement);
}