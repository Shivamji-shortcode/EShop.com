/* Checkout & Razorpay Logic */
document.addEventListener("DOMContentLoaded", function () {
    const payBtn = document.getElementById("rzp-button");
    if (!payBtn) return;

    // We look for a global config object defined in the HTML
    const config = window.razorpayConfig;

    payBtn.addEventListener("click", async function (e) {
        e.preventDefault();

        const address = document.getElementById("address").value.trim();
        const phone = document.getElementById("phone").value.trim();

        if (!address || !phone) {
            alert("⚠️ Please fill in Address and Phone before proceeding!");
            return;
        }

        const response = await fetch(config.createOrderUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": config.csrfToken
            },
            body: JSON.stringify({ amount_rupees: config.totalAmount })
        });

        const data = await response.json();
        const order = data.razorpay_order;

        const options = {
            key: config.razorpayKey,
            amount: order.amount,
            currency: order.currency,
            name: "E-Shop Payments",
            description: "Order Payment",
            order_id: order.id,
            handler: async function (response) {
                const verify = await fetch(config.verifyPaymentUrl, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": config.csrfToken
                    },
                    body: JSON.stringify(response)
                });

                const verifyResult = await verify.json();
                if (verifyResult.status === "success") {
                    alert("✅ Payment Successful!");
                    document.getElementById("checkout-form").submit();
                } else {
                    alert("❌ Payment Verification Failed!");
                }
            },
            config: {
                display: {
                    blocks: {
                        upi: { name: "Pay using UPI", instruments: [{ method: "upi" }] },
                        card: { name: "Pay using Card", instruments: [{ method: "card" }] },
                    },
                    sequence: ["upi", "card"],
                    preferences: { show_default_blocks: true }
                }
            },
            prefill: { contact: phone },
            theme: { color: "#0d6efd" }
        };

        const rzp = new Razorpay(options);
        rzp.open();
    });
});