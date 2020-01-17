(define (problem depotprob26080) (:domain Depot)
(:objects
	depot0 depot1 depot2 depot3 distributor0 distributor1 distributor2 truck0 truck1 truck2 pallet0 pallet1 pallet2 pallet3 pallet4 pallet5 pallet6 crate0 crate1 crate2 crate3 crate4 crate5 crate6 crate7 crate8 crate9 crate10 crate11 crate12 crate13 crate14 crate15 crate16 crate17 hoist0 hoist1 hoist2 hoist3 hoist4 hoist5 hoist6 )
(:init
	(pallet pallet0)
	(surface pallet0)
	(at pallet0 depot0)
	(clear crate3)
	(pallet pallet1)
	(surface pallet1)
	(at pallet1 depot1)
	(clear crate14)
	(pallet pallet2)
	(surface pallet2)
	(at pallet2 depot2)
	(clear crate12)
	(pallet pallet3)
	(surface pallet3)
	(at pallet3 depot3)
	(clear crate13)
	(pallet pallet4)
	(surface pallet4)
	(at pallet4 distributor0)
	(clear crate10)
	(pallet pallet5)
	(surface pallet5)
	(at pallet5 distributor1)
	(clear crate17)
	(pallet pallet6)
	(surface pallet6)
	(at pallet6 distributor2)
	(clear crate15)
	(truck truck0)
	(at truck0 distributor2)
	(truck truck1)
	(at truck1 distributor0)
	(truck truck2)
	(at truck2 depot3)
	(hoist hoist0)
	(at hoist0 depot0)
	(available hoist0)
	(hoist hoist1)
	(at hoist1 depot1)
	(available hoist1)
	(hoist hoist2)
	(at hoist2 depot2)
	(available hoist2)
	(hoist hoist3)
	(at hoist3 depot3)
	(available hoist3)
	(hoist hoist4)
	(at hoist4 distributor0)
	(available hoist4)
	(hoist hoist5)
	(at hoist5 distributor1)
	(available hoist5)
	(hoist hoist6)
	(at hoist6 distributor2)
	(available hoist6)
	(crate crate0)
	(surface crate0)
	(at crate0 distributor2)
	(on crate0 pallet6)
	(crate crate1)
	(surface crate1)
	(at crate1 depot0)
	(on crate1 pallet0)
	(crate crate2)
	(surface crate2)
	(at crate2 distributor0)
	(on crate2 pallet4)
	(crate crate3)
	(surface crate3)
	(at crate3 depot0)
	(on crate3 crate1)
	(crate crate4)
	(surface crate4)
	(at crate4 depot2)
	(on crate4 pallet2)
	(crate crate5)
	(surface crate5)
	(at crate5 depot3)
	(on crate5 pallet3)
	(crate crate6)
	(surface crate6)
	(at crate6 distributor0)
	(on crate6 crate2)
	(crate crate7)
	(surface crate7)
	(at crate7 distributor0)
	(on crate7 crate6)
	(crate crate8)
	(surface crate8)
	(at crate8 depot2)
	(on crate8 crate4)
	(crate crate9)
	(surface crate9)
	(at crate9 depot3)
	(on crate9 crate5)
	(crate crate10)
	(surface crate10)
	(at crate10 distributor0)
	(on crate10 crate7)
	(crate crate11)
	(surface crate11)
	(at crate11 distributor2)
	(on crate11 crate0)
	(crate crate12)
	(surface crate12)
	(at crate12 depot2)
	(on crate12 crate8)
	(crate crate13)
	(surface crate13)
	(at crate13 depot3)
	(on crate13 crate9)
	(crate crate14)
	(surface crate14)
	(at crate14 depot1)
	(on crate14 pallet1)
	(crate crate15)
	(surface crate15)
	(at crate15 distributor2)
	(on crate15 crate11)
	(crate crate16)
	(surface crate16)
	(at crate16 distributor1)
	(on crate16 pallet5)
	(crate crate17)
	(surface crate17)
	(at crate17 distributor1)
	(on crate17 crate16)
	(place depot0)
	(place depot1)
	(place depot2)
	(place depot3)
	(place distributor0)
	(place distributor1)
	(place distributor2)
)

(:goal (and
		(on crate0 crate2)
		(on crate1 crate17)
		(on crate2 pallet2)
		(on crate3 crate9)
		(on crate4 crate16)
		(on crate5 crate8)
		(on crate7 crate11)
		(on crate8 pallet0)
		(on crate9 pallet4)
		(on crate11 pallet3)
		(on crate12 pallet6)
		(on crate13 crate7)
		(on crate15 crate3)
		(on crate16 crate0)
		(on crate17 pallet1)
	)
))
