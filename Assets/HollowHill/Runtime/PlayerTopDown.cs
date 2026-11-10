using UnityEngine;

namespace HollowHill
{
    /// <summary>
    /// Pemain top-down minimal bawaan kit (dipakai menu "5 - Create Player Rig").
    /// Jika Anda sudah punya pemain sendiri, TIDAK perlu komponen ini; cukup pasang HHPlayerHooks.
    /// Konvensi: sprite menghadap +X. AimPivot diputar agar 'right'-nya menunjuk ke mouse.
    /// </summary>
    [RequireComponent(typeof(Rigidbody2D), typeof(HHPlayerHooks))]
    public class PlayerTopDown : MonoBehaviour
    {
        [Header("Gerak (1 unit = 1 tile = sekitar 1,5 m)")]
        public float walkSpeed = 1.9f;
        public float sprintSpeed = 3.4f;

        [Header("Bidik")]
        public Transform aimPivot;
        public Camera cam;

        Rigidbody2D rb;
        Vector2 move;

        void Awake()
        {
            rb = GetComponent<Rigidbody2D>();
            rb.gravityScale = 0f;
            rb.freezeRotation = true;
            rb.collisionDetectionMode = CollisionDetectionMode2D.Continuous;
            rb.interpolation = RigidbodyInterpolation2D.Interpolate;
            if (cam == null) cam = Camera.main;
        }

        void Update()
        {
            move = HHInput.Move();
            Aim();
        }

        void FixedUpdate()
        {
            float speed = HHInput.SprintHeld() ? sprintSpeed : walkSpeed;
            rb.linearVelocity = move * speed;   // Unity 6: linearVelocity (dulu: velocity)
        }

        void Aim()
        {
            if (cam == null || aimPivot == null) return;
            Vector3 sp = HHInput.PointerScreen();
            sp.z = -cam.transform.position.z;
            Vector2 world = cam.ScreenToWorldPoint(sp);
            Vector2 dir = world - (Vector2)aimPivot.position;
            if (dir.sqrMagnitude > 0.0001f) aimPivot.right = dir.normalized;
        }
    }
}
