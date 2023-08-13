$(document).ready(function() {
    const domain = 'https://cu1pfvpkxb.execute-api.eu-west-1.amazonaws.com/prod'
    getUrlVar = function(varName) {
        let vars = [], hash;
        const hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
        for(let i = 0; i < hashes.length; i++) {
            hash = hashes[i].split('=');
            vars.push(hash[0]);
            vars[hash[0]] = hash[1];
        }

        if (vars.includes(varName) === false) {
            alert('Can not find company name in the URL');
            return '';
        }

        return vars[varName];
    }

    const company_name = getUrlVar('company').replace('#', '')
    if (company_name === '') {
        $(".container").hide();
    }

    onOffLoading = function(onOff) {
        $("#loadingModal").css('display', onOff === 1 ? 'block' : 'none');
    }

    makeAPICall = function(query_string, dataHandler) {
        onOffLoading(1);
        const url = domain + '/?company=' + company_name + '&' + query_string;
        $.get(url, function(data, status) {
            dataHandler(data.data)
            onOffLoading(0);
        }).fail(function(jqXHR, textStatus, errorThrown, data) {
            alert("Error: " + jqXHR.responseText);
        });
    }

//    =========================== Image functionalities ===========================
    $("#btnImage").click(function() {
        $("#imageTableBody").empty();
        makeAPICall('action=list-files', displayImages)
        $("#trImage").show();
        $("#trScreen").hide();
    });

    displayImages = function(images) {
        //copy images in the table row
        var i = 0;
        images.forEach(element => {
            i++
            var newRow = $('<tr></tr>');
            newRow.append('<td><a id="imageUrl-'+ i +'" href="' + element.image_url + '" target="_blank">' + element.image_url + '</a><br><button data-imageNumber="'+ i +'">Copy image URL</button></td>');
            newRow.append('<td><img width="150" src="' + element.image_url + '" alt="' + element.image_url + '"></td>');
            $("#imageTableBody").append(newRow);
        });
    }

    $('#imageTableBody').on( 'click', 'button', function (e) {
        //copy image URL to clipboard
        let imageNumber = $(this).attr('data-imageNumber');
        e.preventDefault();
        var copyText = $('#imageUrl-' + imageNumber).attr('href');

        document.addEventListener('copy', function(e) {
            e.clipboardData.setData('text/plain', copyText);
            e.preventDefault();
        }, true);

        document.execCommand('copy');
        console.log('copied text : ', copyText);
    });

//    =========================== Screen functionalities ===========================
    $("#btnScreen").click(function() {
        $("#screenList").empty();
        makeAPICall('action=list-screens', displayScreenList)
        $("#trScreen").show();
        $("#trImage").hide();
    });

    displayScreenList = function(screens) {
        console.log(screens)
    }
});
