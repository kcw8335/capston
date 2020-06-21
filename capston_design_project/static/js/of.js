var already_status = document.querySelector("#already_status")

if (already_status.value == "lock"){
    alert("현재 잠긴 상태입니다.")
} else if (already_status.value == "unlock"){
    alert("현재 열린 상태입니다.")
}