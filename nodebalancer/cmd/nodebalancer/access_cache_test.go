package main

import (
	"testing"
	"time"
)

func accessCacheSetupSuit(t *testing.T) func(t *testing.T) {
	t.Log("Setup suit")

	CreateAccessCache()

	return func(t *testing.T) {
		t.Log("Teardown suit")
	}
}

func TestAddAccessToCache(t *testing.T) {
	teardownSuit := accessCacheSetupSuit(t)
	defer teardownSuit(t)

	tsNow := time.Now().Unix()

	var cases = []struct {
		prop     ClientAccess
		expected bool
	}{
		{
			prop:     ClientAccess{ClientResourceData: ClientResourceData{AccessID: "7378e2b2-b6ac-4738-bf34-fe39aa0d19e9"}},
			expected: true,
		},
		{
			prop:     ClientAccess{ClientResourceData: ClientResourceData{AccessID: "000000000000000000000000000000000000"}},
			expected: false,
		},
		{
			prop:     ClientAccess{ClientResourceData: ClientResourceData{Name: "name-1"}},
			expected: false,
		},
	}
	for _, c := range cases {
		accessId := c.prop.ClientResourceData.AccessID
		accessCache.AddAccessToCache(c.prop, tsNow)
		if accessCache.isAccessIdInCache(accessId) != c.expected {
			t.Logf("Access %s not found in access cache", accessId)
			t.Fatal()
		}
	}
}
