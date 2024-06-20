package hbd.service.domain.entity

import jakarta.persistence.Column
import jakarta.persistence.Entity
import jakarta.persistence.Id
import jakarta.persistence.Table
import java.time.LocalDateTime

@Entity
@Table(name = "deliveries")
class DeliveryEntity(
    @Id
    val deliveryId: String,
    @Column(name = "order_date_created")
    val orderDateCreated: LocalDateTime,
    @Column(name = "order_id")
    val orderId: String,
    @Column(name = "deliveryman_id")
    val deliveryManId: String,
    @Column(name = "delivery_address")
    val deliveryAddress: String,
    @Column(name = "delivery_time")
    val deliveryTime: LocalDateTime,
    val rating: Double,
    val tips: Double?
)
