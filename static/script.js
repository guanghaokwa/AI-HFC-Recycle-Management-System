url = window.location.href

url_list = url.split(":5000")

const video = document.getElementById("live-video");
const canvas = document.getElementById("detection-overlay");
//const ctx = canvas.getContext("2d");
const detectionResults = document.getElementById("detection-results");

// Start video stream
if (url_list[1] == '/') {
    navigator.mediaDevices
        .getUserMedia({ video: true })
        .then((stream) => {
            video.srcObject = stream;
        })
        .catch((err) => {
            console.error("Error accessing webcam:", err);
        });

    window.onload = () => {
        let str_value = document.getElementById('form_info').value
        console.log(str_value)
        if (str_value == 'hide') {
            document.getElementById('upload_video').style.display = "none"
            document.getElementById('upload_form').style.display = "none"
            document.getElementById('qrcode_container').style.display = "block"
            document.getElementById('qrcode-info').style.display = "block"

            setTimeout(() => {
                document.getElementById('upload_video').style.display = "block"
                document.getElementById('upload_form').style.display = "block"
                document.getElementById('qrcode_container').style.display = "none"
                document.getElementById('qrcode-info').style.display = "block"

                document.getElementById('form_info').value = 'not yet'

                window.location.href = '/qrcode'
            }, 10000);
        } else {
            document.getElementById('upload_video').style.display = "block"
            document.getElementById('upload_form').style.display = "block"
            document.getElementById('qrcode_container').style.display = "none"
            document.getElementById('qrcode-info').style.display = "block"
        }
        
    }
}

function navigateTo(value) {
    if (value) {
        window.location.href = value;
    }
}

// function sendMessage() {
//     const input = document.getElementById('chat-input');
//     const chatDisplay = document.getElementById('chat-display');

//     if (input.value.trim()) {
//         const userMessage = document.createElement('div');
//         userMessage.className = 'message user-message';
//         userMessage.textContent = input.value;
//         chatDisplay.appendChild(userMessage);

//         const botMessage = document.createElement('div');
//         botMessage.className = 'message bot-message';
//         botMessage.textContent = "I'm sorry, I didn't understand that.";
//         chatDisplay.appendChild(botMessage);

//         input.value = '';
//         chatDisplay.scrollTop = chatDisplay.scrollHeight;
//     }
// }
