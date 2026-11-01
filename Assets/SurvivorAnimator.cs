using UnityEngine;

public class SurvivorAnimator : MonoBehaviour
{
    [SerializeField] private Rigidbody2D body;
    [SerializeField] private Animator bodyAnimator;

    void Update()
    {
        float speed = body.linearVelocity.magnitude;
        bodyAnimator.SetFloat("Speed", speed);
    }
}