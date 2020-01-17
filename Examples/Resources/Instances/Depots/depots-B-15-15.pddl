(define (problem depotprob29784) (:domain Depot)
(:objects
	depot0 depot1 depot2 depot3 depot4 distributor0 distributor1 distributor2 distributor3 truck0 truck1 truck2 truck3 pallet0 pallet1 pallet2 pallet3 pallet4 pallet5 pallet6 pallet7 pallet8 crate0 crate1 crate2 crate3 crate4 crate5 crate6 crate7 crate8 crate9 crate10 crate11 crate12 crate13 crate14 hoist0 hoist1 hoist2 hoist3 hoist4 hoist5 hoist6 hoist7 hoist8 )
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
	(clear crate13)
	(pallet pallet3)
	(surface pallet3)
	(at pallet3 depot3)
	(clear crate10)
	(pallet pallet4)
	(surface pallet4)
	(at pallet4 depot4)
	(clear crate6)
	(pallet pallet5)
	(surface pallet5)
	(at pallet5 distributor0)
	(clear pallet5)
	(pallet pallet6)
	(surface pallet6)
	(at pallet6 distributor1)
	(clear crate12)
	(pallet pallet7)
	(surface pallet7)
	(at pallet7 distributor2)
	(clear crate7)
	(pallet pallet8)
	(surface pallet8)
	(at pallet8 distributor3)
	(clear pallet8)
	(truck truck0)
	(at truck0 depot0)
	(truck truck1)
	(at truck1 distributor1)
	(truck truck2)
	(at truck2 depot3)
	(truck truck3)
	(at truck3 distributor1)
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
	(at crate0 distributor1)
	(on crate0 pallet6)
	(crate crate1)
	(surface crate1)
	(at crate1 distributor1)
	(on crate1 crate0)
	(crate crate2)
	(surface crate2)
	(at crate2 distributor1)
	(on crate2 crate1)
	(crate crate3)
	(surface crate3)
	(at crate3 depot0)
	(on crate3 pallet0)
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
	(at crate6 depot4)
	(on crate6 pallet4)
	(crate crate7)
	(surface crate7)
	(at crate7 distributor2)
	(on crate7 pallet7)
	(crate crate8)
	(surface crate8)
	(at crate8 depot1)
	(on crate8 pallet1)
	(crate crate9)
	(surface crate9)
	(at crate9 depot3)
	(on crate9 crate5)
	(crate crate10)
	(surface crate10)
	(at crate10 depot3)
	(on crate10 crate9)
	(crate crate11)
	(surface crate11)
	(at crate11 distributor1)
	(on crate11 crate2)
	(crate crate12)
	(surface crate12)
	(at crate12 distributor1)
	(on crate12 crate11)
	(crate crate13)
	(surface crate13)
	(at crate13 depot2)
	(on crate13 crate4)
	(crate crate14)
	(surface crate14)
	(at crate14 depot1)
	(on crate14 crate8)
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
		(on crate0 crate12)
		(on crate1 pallet6)
		(on crate2 crate0)
		(on crate3 crate11)
		(on crate4 pallet1)
		(on crate5 crate7)
		(on crate6 pallet4)
		(on crate7 pallet8)
		(on crate8 crate13)
		(on crate9 pallet2)
		(on crate11 crate8)
		(on crate12 pallet7)
		(on crate13 pallet0)
		(on crate14 crate1)
	)
))
