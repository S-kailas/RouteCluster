
// ================= CONFIG =================
const BASE_URL = "http://VPSip:800"   // ← CHANGE if needed
// =========================================


// Initialize map
let map = L.map('map').setView([8.54, 76.90], 12)

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19
}).addTo(map)

let markers = []
let polylines = []


// Clear map
function clearMap() {
    markers.forEach(m => map.removeLayer(m))
    polylines.forEach(p => map.removeLayer(p))

    markers = []
    polylines = []
}


// Upload file
async function uploadFile() {

    let fileInput = document.getElementById("excelFile")

    if (!fileInput.files.length) {
        alert("Upload Excel File")
        return
    }

    let formData = new FormData()
    formData.append("file", fileInput.files[0])

    try {

        let response = await fetch(`${BASE_URL}/upload`, {
            method: "POST",
            body: formData
        })

        if (!response.ok) {
            alert("Upload failed")
            return
        }

        let data = await response.json()

        if (!data.clusters) {
            alert("Invalid response from server")
            return
        }

        displayClusters(data.clusters)

    } catch (error) {
        console.error(error)
        alert("Server error")
    }
}


// Display clusters
function displayClusters(clusters) {

    clearMap()

    let colors = ["red", "blue", "green", "orange", "purple", "black"]

    let allPoints = []

    clusters.forEach((cluster, index) => {

        let color = colors[index % colors.length]

        // ---------- MARKERS ----------
        cluster.points.forEach(p => {

            let latlng = [p.lat, p.lng]

            let marker = L.circleMarker(latlng, {
                radius: 8,
                color: color,
                fillColor: color,
                fillOpacity: 0.8
            }).addTo(map)

            marker.bindPopup(`Cluster ${cluster.cluster_id}<br>Order: ${p.order}`)

            markers.push(marker)
            allPoints.push(latlng)
        })

        // ---------- ROUTE ----------
        if (cluster.geometry && cluster.geometry.length > 0) {

            // Real OSRM route
            let polyline = L.polyline(cluster.geometry, {
                color: color,
                weight: 4
            }).addTo(map)

            polylines.push(polyline)

        } else {

            // Fallback (straight line)
            let fallback = cluster.points
                .sort((a, b) => a.order - b.order)
                .map(p => [p.lat, p.lng])

            let polyline = L.polyline(fallback, {
                color: color,
                dashArray: "5,5",
                weight: 3
            }).addTo(map)

            polylines.push(polyline)
        }

    })

    // ---------- AUTO ZOOM ----------
    if (allPoints.length > 0) {
        map.fitBounds(allPoints)
    }
}


// Download Excel
function downloadExcel() {
    window.open(`${BASE_URL}/download`)
}

