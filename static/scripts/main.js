
$(document).ready(function () {
    $(":file").change(function () {
        if (this.files && this.files[0]) {

            var reader = new FileReader();
            reader.onload = imageIsLoaded;
            reader.readAsDataURL(this.files[0]);
        }
    });
    rangeSlider()
});

function imageIsLoaded(e) {
    $('#myImg').attr('src', e.target.result);
};

function detect(element) {
    var detectionImg = document.getElementById("myImg")
    if (detectionImg.src == "http://127.0.0.1:5000/") {
        alert('please load an image')
    }
    else {
        var file = document.getElementById("upload").files[0];
        var reader = new FileReader();
        reader.onloadend = function () {
            performDetection(reader.result, element.id)
        }
        reader.readAsDataURL(file);
    }

}
function performDetection(src, classID) {
    document.getElementsByClassName("loader")[0].style.display = "block"
    jQuery.ajax({
        url: "/runDetection",
        type: "POST",
        data: JSON.stringify({ "src": src, "class": classID }),
        dataType: "json",
        contentType: "application/json",
        success: function (e) {
            img = new Image()
            img.src = "/static/images/detection.jpg?dave=" + Math.floor(Math.random() * 1000).toString();
            img.onload = function () {
                document.getElementById("myImg").src = img.src
                document.getElementById("total").innerHTML = "Total: " + "£" + e.total
                document.getElementsByClassName("loader")[0].style.display = "none"
            }
        },
        error: function (error) {
            console.log("error")
        },
    });
}


function changeConfidence(element) {
    jQuery.ajax({
        url: "/setConfidence",
        type: "POST",
        data: JSON.stringify(element.value),
        dataType: "json",
        contentType: "application/json",
        success: function (e) {
            console.log("success")
        },
        error: function (error) {
            console.log("error")
        },
    });

}

function openCamera() {
    document.getElementById("robotcell").style.display = "block"
    document.getElementById("robotcell").src = "/video_feed"
    document.getElementById("myImg").style.display = "none"
}

function unhideImage() {
    document.getElementById("robotcell").style.display = "none"
    document.getElementById("robotcell").src = ""
    document.getElementById("myImg").style.display = "block"
}

var rangeSlider = function () {
    var slider = $(".range-slider"),
        range = $('.range-slider input[type="range"]'),
        value = $(".range-value");
    slider.each(function () {
        value.each(function () {
            var value = $(this).prev().attr("value");
            $(this).html(value);
        });
        range.on("input", function () {
            $(this).next(value).html(this.value);
        });
    });
};
