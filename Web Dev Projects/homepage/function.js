document.addEventListener('DOMContentLoaded', function () {
    var myhome = document.getElementById('myhome');
    myhome.addEventListener('click', function (e) {
        e.preventDefault();
        map.setView([-6.34, 106.93], 13);
        L.marker([-6.34, 106.93]).addTo(map);
    });
});