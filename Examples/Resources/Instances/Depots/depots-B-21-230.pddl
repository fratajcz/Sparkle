(define (problem depotprob8019) (:domain Depot)
(:objects
	depot0 depot1 depot2 depot3 depot4 distributor0 distributor1 distributor2 distributor3 truck0 truck1 truck2 truck3 pallet0 pallet1 pallet2 pallet3 pallet4 pallet5 pallet6 pallet7 pallet8 crate0 crate1 crate2 crate3 crate4 crate5 crate6 crate7 crate8 crate9 crate10 crate11 crate12 crate13 crate14 crate15 crate16 crate17 crate18 crate19 crate20 hoist0 hoist1 hoist2 hoist3 hoist4 hoist5 hoist6 hoist7 hoist8 )
(:init
	(pallet pallet0)
	(surface pallet0)
	(at pallet0 depot0)
	(clear crate17)
	(pallet pallet1)
	(surface pallet1)
	(at pallet1 depot1)
	(clear crate20)
	(pallet pallet2)
	(surface pallet2)
	(at pallet2 depot2)
	(clear crate19)
	(pallet pallet3)
	(surface pallet3)
	(at pallet3 depot3)
	(clear crate18)
	(pallet pallet4)
	(surface pallet4)
	(at pallet4 depot4)
	(clear crate5)
	(pallet pallet5)
	(surface pallet5)
	(at pallet5 distributor0)
	(clear crate16)
	(pallet pallet6)
	(surface pallet6)
	(at pallet6 distributor1)
	(clear crate9)
	(pallet pallet7)
	(surface pallet7)
	(at pallet7 distributor2)
	(clear crate14)
	(pallet pallet8)
	(surface pallet8)
	(at pallet8 distributor3)
	(clear crate13)
	(truck truck0)
	(at truck0 depot0)
	(truck truck1)
	(at truck1 distributor1)
	(truck truck2)
	(at truck2 distributor3)
	(truck truck3)
	(at truck3 depot1)
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
	(at hoist4 depot4)
	(available hoist4)
	(hoist hoist5)
	(at hoist5 distributor0)
	(available hoist5)
	(hoist hoist6)
	(at hoist6 distributor1)
	(available hoist6)
	(hoist hoist7)
	(at hoist7 distributor2)
	(available hoist7)
	(hoist hoist8)
	(at hoist8 distributor3)
	(available hoist8)
	(crate crate0)
	(surface crate0)
	(at crate0 distributor0)
	(on crate0 pallet5)
	(crate crate1)
	(surface crate1)
	(at crate1 depot2)
	(on crate1 pallet2)
	(crate crate2)
	(surface crate2)
	(at crate2 depot4)
	(on crate2 pallet4)
	(crate crate3)
	(surface crate3)
	(at crate3 distributor3)
	(on crate3 pallet8)
	(crate crate4)
	(surface crate4)
	(at crate4 distributor1)
	(on crate4 pallet6)
	(crate crate5)
	(surface crate5)
	(at crate5 depot4)
	(on crate5 crate2)
	(crate crate6)
	(surface crate6)
	(at crate6 distributor0)
	(on crate6 crate0)
	(crate crate7)
	(surface crate7)
	(at crate7 depot1)
	(on crate7 pallet1)
	(crate crate8)
	(surface crate8)
	(at crate8 depot1)
	(on crate8 crate7)
	(crate crate9)
	(surface crate9)
	(at crate9 distributor1)
	(on crate9 crate4)
	(crate crate10)
	(surface crate10)
	(at crate10 distributor2)
	(on crate10 pallet7)
	(crate crate11)
	(surface crate11)
	(at crate11 distributor2)
	(on crate11 crate10)
	(crate crate12)
	(surface crate12)
	(at crate12 distributor3)
	(on crate12 crate3)
	(crate crate13)
	(surface crate13)
	(at crate13 distributor3)
	(on crate13 crate12)
	(crate crate14)
	(surface crate14)
	(at crate14 distributor2)
	(on crate14 crate11)
	(crate crate15)
	(surface crate15)
	(at crate15 depot3)
	(on crate15 pallet3)
	(crate crate16)
	(surface crate16)
	(at crate16 distributor0)
	(on crate16 crate6)
	(crate crate17)
	(surface crate17)
	(at crate17 depot0)
	(on crate17 pallet0)
	(crate crate18)
	(surface crate18)
	(at crate18 depot3)
	(on crate18 crate15)
	(crate crate19)
	(surface crate19)
	(at crate19 depot2)
	(on crate19 crate1)
	(crate crate20)
	(surface crate20)
	(at crate20 depot1)
	(on crate20 crate8)
	(place depot0)
	(place depot1)
	(place depot2)
	(place depot3)
	(place depot4)
	(place distributor0)
	(place distributor1)
	(place distributor2)
	(place distributor3)
)

(:goal (and
		(on crate0 crate8)
		(on crate1 pallet5)
		(on crate3 crate20)
		(on crate4 crate14)
		(on crate5 pallet3)
		(on crate6 crate19)
		(on crate7 crate16)
		(on crate8 crate15)
		(on crate9 pallet6)
		(on crate10 crate9)
		(on crate11 crate5)
		(on crate13 pallet2)
		(on crate14 pallet1)
		(on crate15 pallet8)
		(on crate16 crate6)
		(on crate17 pallet4)
		(on crate18 pallet0)
		(on crate19 crate4)
		(on crate20 crate17)
	)
))
