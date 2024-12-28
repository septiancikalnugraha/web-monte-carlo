document.addEventListener("DOMContentLoaded", function () {
    const loadingMessage = document.getElementById("loading-message");
    const dataTbody = document.getElementById("data-tbody");

    // Tampilkan pesan loading sebelum tabel dimuat
    if (dataTbody.children.length === 0) {
        loadingMessage.style.display = "block";
    } else {
        loadingMessage.style.display = "none";
    }

    // Fungsi untuk filter data tabel
    const filterInput = document.createElement("input");
    filterInput.type = "text";
    filterInput.placeholder = "Cari tahun atau jumlah...";
    filterInput.addEventListener("keyup", function () {
        const filterValue = filterInput.value.toLowerCase();
        const rows = dataTbody.getElementsByTagName("tr");
        for (let i = 0; i < rows.length; i++) {
            const cells = rows[i].getElementsByTagName("td");
            const match = Array.from(cells).some((cell) =>
                cell.textContent.toLowerCase().includes(filterValue)
            );
            rows[i].style.display = match ? "" : "none";
        }
    });

    const section = document.querySelector("section");
    section.insertBefore(filterInput, section.firstChild);
}); 