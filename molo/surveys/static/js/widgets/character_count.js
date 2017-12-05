(function() {
    document.addEventListener('DOMContentLoaded', function() {
        var inputs = document.querySelectorAll('.input-group input[type="text"]');
        var setSpanValue = function(target) {
            var span = target.nextSibling;
            // If the value next to the input is not a span, skip
            if (!span || span.nodeName.toLowerCase() !== 'span') {
                return;
            }
            var limit = parseInt(target.getAttribute('maxlength'));
            var current = target.value.length;
            var remaining = limit - current;
            span.textContent = remaining;
        };
        for (var i = 0; i < inputs.length; i++) {
            setSpanValue(inputs[i]);
            inputs[i].addEventListener("input", function(e) {
                setSpanValue(e.target);
            },false);
        }
    }, false);
})();
