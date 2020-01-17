(define (problem depotprob22610) (:domain Depot)
(:objects
	depot0 depot1 depot2 depot3 depot4 distributor0 distributor1 distributor2 distributor3 truck0 truck1 truck2 truck3 pallet0 pallet1 pallet2 pallet3 pallet4 pallet5 pallet6 pallet7 pallet8 crate0 crate1 crate2 crate3 crate4 crate5 crate6 crate7 crate8 crate9 crate10 crate11 crate12 crate13 crate14 hoist0 hoist1 hoist2 hoist3 hoist4 hoist5 hoist6 hoist7 hoist8 )
(:init
	(pallet pallet0)
	(surface pallet0)
	(at pallet0 depot0)
	(clear crate11)
	(pallet pallet1)
	(surface pallet1)
	(at pallet1 depot1)
	(clear crate10)
	(pallet pallet2)
	(surface pallet2)
	(at pallet2 depot2)
	(clear crate8)
	(pallet pallet3)
	(surface pallet3)
	(at pallet3 depot3)
	(clear crate1)
	(pallet pallet4)
	(surface pallet4)
	(at pallet4 depot4)
	(clear crate13)
	(pallet pallet5)
	(surface pallet5)
	(at pallet5 distributor0)
	(clear pallet5)
	(pallet pallet6)
	(surface pallet6)
	(at pallet6 distributor1)
	(clear crate7)
	(pallet pallet7)
	(surface pallet7)
	(at pallet7 distributor2)
	(clear crate14)
	(pallet pallet8)
	(surface pallet8)
	(at pallet8 distributor3)
	(clear crate12)
	(truck truck0)
	(at truck0 depot4)
	(truck truck1)
	(at truck1 distributor3)
	(truck truck2)
	(at truck2 distributor0)
	(truck truck3)
	(at truck3 depot4)
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
	(at crate0 depot1)
	(on crate0 pallet1)
	(crate crate1)
	(surface crate1)
	(at crate1 depot3)
	(on crate1 pallet3)
	(crate crate2)
	(surface crate2)
	(at crate2 depot2)
	(on crate2 pallet2)
	(crate crate3)
	(surface crate3)
	(at crate3 depot2)
	(on crate3 crate2)
	(crate crate4)
	(surface crate4)
	(at crate4 distributor1)
	(on crate4 pallet6)
	(crate crate5)
	(surface crate5)
	(at crate5 depot2)
	(on crate5 crate3)
	(crate crate6)
	(surface crate6)
	(at crate6 distributor3)
	(on crate6 pallet8)
	(crate crate7)
	(surface crate7)
	(at crate7 distributor1)
	(on crate7 crate4)
	(crate crate8)
	(surface crate8)
	(at crate8 depot2)
	(on crate8 crate5)
	(crate crate9)
	(surface crate9)
	(at crate9 depot4)
	(on crate9 pallet4)
	(crate crate10)
	(surface crate10)
	(at crate10 depot1)
	(on crate10 crate0)
	(crate crate11)
	(surface crate11)
	(at crate11 depot0)
	(on crate11 pallet0)
	(crate crate12)
	(surface crate12)
	(at crate12 distributor3)
	(on crate12 crate6)
	(crate crate13)
	(surface crate13)
	(at crate13 depot4)
	(on crate13 crate9)
	(crate crate14)
	(surface crate14)
	(at crate14 distributor2)
	(on crate14 pallet7)
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
		(on crate0 crate11)
		(on crate1 crate3)
		(on crate3 crate8)
		(on crate4 crate13)
		(on crate5 crate0)
		(on crate7 pallet3)
		(on crate8 pallet8)
		(on crate9 crate12)
		(on crate10 pallet2)
		(on crate11 pallet5)
		(on crate12 pallet4)
		(on crate13 crate10)
		(on crate14 pallet0)
	)
))
