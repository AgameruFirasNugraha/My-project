using UnityEngine;

namespace HollowHill
{
    public enum PickupKind { Key, Battery, Note }

    public class PickupItem : MonoBehaviour
    {
        public PickupKind kind = PickupKind.Key;
        public string keyId = "";
        public float batterySeconds = 60f;
        [TextArea] public string noteText = "";
        public AudioClip pickupClip;

        // Fungsi ini akan dipanggil otomatis oleh WorldItem -> On Picked Up ()
        public void TriggerPickup()
        {
            var player = FindAnyObjectByType<HHPlayerHooks>();
            if (player == null) return;

            switch (kind)
            {
                case PickupKind.Key:
                    player.AddKey(keyId);
                    Debug.Log("[HollowHill] Mengambil kunci '" + keyId + "'");
                    break;
                case PickupKind.Battery:
                    var f = player.GetComponentInChildren<FlashlightController>();
                    if (f != null) f.AddBattery(batterySeconds);
                    break;
                case PickupKind.Note:
                    Debug.Log("[CATATAN] " + noteText);
                    break;
            }

            if (pickupClip != null) AudioSource.PlayClipAtPoint(pickupClip, transform.position);
        }
    }
}
