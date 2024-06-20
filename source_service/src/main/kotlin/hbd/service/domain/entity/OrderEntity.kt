package hbd.service.domain.entity

import jakarta.persistence.*
import java.time.LocalDateTime
import java.util.*

@Entity
@Table(name = "orders")
class OrderEntity(
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    val id: UUID,
    @Column(name = "order_date_created")
    val orderDateCreated: LocalDateTime,
    @Column(name = "delivery_id")
    val deliveryId: String,
    @Column(name = "deliveryman_id")
    val deliveryManId: String,
    @Column(name = "delivery_address")
    val deliveryAddress: String,
    @Column(name = "delivery_time")
    val deliveryTime: LocalDateTime,
    val rating: Double,
    val tips: Double?
)
