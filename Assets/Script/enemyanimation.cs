using UnityEngine;

public class EnemyAnimation : MonoBehaviour
{
    private Animator anim;
    private Vector3 lastPosition;

    void Start()
    {
        anim = GetComponent<Animator>();
        lastPosition = transform.position;
    }

    void Update()
    {
        // Gerak = posisi berubah dibanding frame sebelumnya
        bool isMoving = (transform.position - lastPosition).sqrMagnitude > 0.00001f;
        anim.SetBool("iswalking", isMoving);
        lastPosition = transform.position;
    }
}