using System.Collections.Generic;
using UnityEngine;

namespace HollowHill
{
    public interface IInteractable
    {
        string Prompt { get; }
        void Interact(HHPlayerHooks who);
    }

    /// <summary>
    /// Pasang di objek pemain MILIK ANDA (mis. PlayerController). Fungsinya tiga:
    /// 1) penanda "ini pemain" bagi pintu, zona suasana, dan atap;
    /// 2) tempat menyimpan kunci;
    /// 3) tombol E untuk berinteraksi dengan objek IInteractable terdekat (pintu).
    /// Tidak mengubah skrip gerak atau senter Anda.
    /// </summary>
    public class HHPlayerHooks : MonoBehaviour
    {
        public float interactRadius = 1.1f;

        readonly HashSet<string> keys = new HashSet<string>();
        readonly Collider2D[] hits = new Collider2D[16];

        public bool HasKey(string id) { return !string.IsNullOrEmpty(id) && keys.Contains(id); }
        public void AddKey(string id) { if (!string.IsNullOrEmpty(id)) keys.Add(id); }

        void Update()
        {
            if (HHInput.InteractDown()) TryInteract();
        }

        void TryInteract()
        {
            var filter = new ContactFilter2D();
            filter.NoFilter();   // termasuk trigger
            int n = Physics2D.OverlapCircle(transform.position, interactRadius, filter, hits);
            IInteractable best = null;
            float bestD = float.MaxValue;
            for (int i = 0; i < n; i++)
            {
                var it = hits[i].GetComponentInParent<IInteractable>();
                if (it == null) continue;
                float d = ((Vector2)hits[i].transform.position - (Vector2)transform.position).sqrMagnitude;
                if (d < bestD) { bestD = d; best = it; }
            }
            if (best != null) best.Interact(this);
        }
    }
}
