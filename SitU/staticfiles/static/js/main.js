function showLoginAlert(loginUrl) {
    // 기존 모달이 있다면 제거
    var existingModal = document.getElementById('customModal');
    if (existingModal) {
        existingModal.remove();
    }

    // 새 모달 생성
    var modal = document.createElement('div');
    modal.id = 'customModal';
    modal.className = 'custom-modal';
    modal.innerHTML = `
        <div class="modal-content">
            <p class="modal-message">'관심&즐겨찾기' 기능은<br>로그인 후에 사용 가능합니다.</p>
            <button class="modal-button">확인</button>
        </div>
    `;

    // 모달을 body에 추가
    document.body.appendChild(modal);

    // 모달 표시
    modal.style.display = 'block';

    // 확인 버튼 클릭 시 로그인 페이지로 이동
    modal.querySelector('.modal-button').onclick = function () {
        window.location.href = loginUrl;
    };

    // 모달 외부 클릭 시 닫기
    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    };
}
