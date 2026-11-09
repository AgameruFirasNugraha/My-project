using UnityEngine;
using UnityEngine.Rendering.Universal;

namespace HollowHill
{
    /// <summary>
    /// Pintu interaktif (tekan E dekat pintu). Tertutup: sprite tutup + collider aktif + menghalangi cahaya.
    /// Terbuka: sprite buka (punya overhang daun pintu) + collider & shadow mati.
    /// Pivot sprite pintu sudah diatur importer agar sel pintu selalu pas di grid.
    /// </summary>
    public class Door2D : MonoBehaviour, IInteractable
    {
        [Header("Visual")]
        public SpriteRenderer spriteRenderer;
        public Sprite closedSprite;
        public Sprite openSprite;

        [Header("Penghalang")]
        public Collider2D blocker;
        public ShadowCaster2D shadow;

        [Header("Aturan")]
        public bool startsOpen;
        public bool locked;
        public string requiredKeyId = "";

        [Header("Audio (opsional)")]
        public AudioSource audioSource;
        public AudioClip openClip, closeClip, lockedClip;

        public bool IsOpen { get; private set; }
        public string Prompt { get { return locked ? "Terkunci" : (IsOpen ? "Tutup" : "Buka"); } }

        void Start() { Apply(startsOpen); }

        public void Interact(HHPlayerHooks who)
        {
            if (locked)
            {
                bool hasKey = who != null && who.HasKey(requiredKeyId);
                if (!hasKey)
                {
                    Debug.Log("[HollowHill] Pintu terkunci. Butuh kunci: '" + requiredKeyId + "'");
                    Play(lockedClip);
                    return;
                }
                locked = false;
                Debug.Log("[HollowHill] Pintu dibuka dengan kunci '" + requiredKeyId + "'");
            }
            Apply(!IsOpen);
            Play(IsOpen ? openClip : closeClip);
        }

        void Apply(bool open)
        {
            IsOpen = open;
            if (spriteRenderer != null) spriteRenderer.sprite = open ? openSprite : closedSprite;
            if (blocker != null) blocker.enabled = !open;
            if (shadow != null) shadow.enabled = !open;
        }

        void Play(AudioClip c) { if (audioSource != null && c != null) audioSource.PlayOneShot(c); }
    }
}
