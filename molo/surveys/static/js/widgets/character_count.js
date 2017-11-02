(function() {
    document.addEventListener('DOMContentLoaded', function() {
        var inputs = document.querySelectorAll('.input-group input[type="text"]');
        var span = document.createElement('span');
        var setSpanValue = function(target) {
            var limit = parseInt(target.getAttribute('maxlength'));
            var current = target.value.length;
            var remaining = limit - current;
            span.textContent = remaining;
        };
        for (var i = 0; i < inputs.length; i++) {
            inputs[i].parentNode.insertBefore(span, inputs[i].nextSibling);
            setSpanValue(inputs[i]);
            inputs[i].addEventListener("input", function(e) {
                setSpanValue(e.target);
            },false);
        }
    }, false);
})();