using UnityEngine;

namespace HollowHill
{
    public enum PickupKind { Key, Battery, Note }

    [RequireComponent(typeof(Collider2D))]
    public class PickupItem : MonoBehaviour
    {
        public PickupKind kind = PickupKind.Key;
        public string keyId = "";
        public float batterySeconds = 60f;
        [TextArea] public string noteText = "";
        public AudioClip pickupClip;

        void Reset() { GetComponent<Collider2D>().isTrigger = true; }

        void OnTriggerEnter2D(Collider2D other)
        {
            var player = other.GetComponentInParent<HHPlayerHooks>();
            if (player == null) return;

            switch (kind)
            {
                case PickupKind.Key:
                    player.AddKey(keyId);
                    Debug.Log("[HollowHill] Mengambil kunci '" + keyId + "'");
                    break;
                case PickupKind.Battery:
                    // Bekerja dengan FlashlightController bawaan kit. Untuk senter buatan sendiri,
                    // panggil fungsi isi baterai Anda di sini.
                    var f = player.GetComponentInChildren<FlashlightController>();
                    if (f != null) f.AddBattery(batterySeconds);
                    break;
                case PickupKind.Note:
                    Debug.Log("[CATATAN] " + noteText);   // ganti dengan UI catatan Anda
                    break;
            }
            if (pickupClip != null) AudioSource.PlayClipAtPoint(pickupClip, transform.position);
            Destroy(gameObject);
        }
    }
}
