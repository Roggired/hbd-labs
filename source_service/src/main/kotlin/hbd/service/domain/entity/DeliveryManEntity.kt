package hbd.service.domain.entity

import jakarta.persistence.Entity
import jakarta.persistence.Id
import jakarta.persistence.Table

@Entity
@Table(name = "delivery_man")
class DeliveryManEntity (
    @Id
    val id: String,
    val name: String
)
