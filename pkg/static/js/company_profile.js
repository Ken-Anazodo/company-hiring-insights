document.addEventListener("DOMContentLoaded", function () {
    var selectedDiv = document.querySelector(".selected");
    var optionsContainer = document.querySelector(".options");
    var optionLabels = document.querySelectorAll(".option");
    var rolesChart = echarts.init(document.getElementById("roles-chart"));
    var citiesChart = echarts.init(document.getElementById("cities-chart"));

    rolesChart.setOption({
        textStyle: {
            color: '#ff6926' // Custom orange color
          },
        title: { text: "Job Roles Distribution", left: "center", textStyle: {
            color: '#ff6926',
          } },
        tooltip: { trigger: "axis" },
        xAxis: { type: "value" },
        yAxis: { 
            type: "category",
            data: rolesData.map((item) => item.name)
        },
        grid: {
            left: '9%',
            right: '4%',
            bottom: '3%',
            containLabel: true
          },
        series: [{ 
            name: "Job Roles", 
            type: "bar",
            data: rolesData.map((item) => item.value), 
            itemStyle: { color: "#925E29" }
        }],
    });

    citiesChart.setOption({
        textStyle: {
            color: '#ff6926' // Custom orange color
          },
        title: { text: "Job Postings by City", left: "center", textStyle: {
            color: '#ff6926',
          }},
        tooltip: { trigger: "item" },
        xAxis: { type: "category", data: citiesData.map((item) => item.name), axisLabel: { rotate: 30 } },
        yAxis: { type: "value", name: "Job Postings" },
        series: [{
            name: "Job Postings",
            type: "scatter",
            symbolSize: (val) => val[1] / 50,
            data: citiesData.map((item) => [item.name, item.value]),
            itemStyle: { color: "#925E29" },
        }],
    });


    

    selectedDiv.addEventListener("click", function () {
        optionsContainer.classList.toggle("hidden");
    });

    optionLabels.forEach(label => {
        label.addEventListener("click", function () {
            var selectedCompany = this.getAttribute("data-value");

            if (selectedCompany) {
                selectedDiv.textContent = selectedCompany;
                optionsContainer.classList.add("hidden");

                // Redirect to new page (Full Page Reload)
                window.location.href = `/company/${encodeURIComponent(selectedCompany)}/`;
            }
        });
    });

    document.addEventListener("click", function (event) {
        if (!selectedDiv.contains(event.target) && !optionsContainer.contains(event.target)) {
            optionsContainer.classList.add("hidden");
        }
    });
});
