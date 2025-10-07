// bot/routes/webhook.js
import express from "express";
const router = express.Router();

router.post("/payment-webhook", async (req, res) => {
  const { tenant, phone, amount, invoice_id, date } = req.body;

  const msg = `✅ Rent Payment Received\n\nTenant: ${tenant}\nAmount: ${amount}\nInvoice: ${invoice_id}\nDate: ${date}`;

  try {
    await sock.sendMessage(`${phone}@s.whatsapp.net`, { text: msg });
    res.json({ success: true });
  } catch (err) {
    console.error("WhatsApp send error:", err);
    res.status(500).json({ error: "failed to send" });
  }
});

export default router;

