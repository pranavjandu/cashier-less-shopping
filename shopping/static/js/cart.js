var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function () {
		var productId = this.dataset.product
		var action = this.dataset.action

			updateUserOrder(productId, action)
	})
}

function updateUserOrder(productId, action) {
	$.ajax({
		url: '/addtocart',
		data: {
			'productid': productId,
			'action': action
		},
		dataType: 'json',
		success: function (data) {
			location.reload()
		}
	});
}

