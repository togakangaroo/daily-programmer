// Simple implementation tests
// :PROPERTIES:
// :header-args:go+: :tangle arithmetic_progression_test.go
// :END:

// Lets write some tests

// [[file:README.org::*Simple implementation tests][Simple implementation tests:1]]
package main


import (
	"testing"
)

func TestIsArithmeticProgression(t *testing.T) {
	testCases := []struct {
		name     string
		input    []int
		expected bool
	}{
		{"Example 1 - Valid progression", []int{3, 5, 1}, true},
		{"Example 2 - Invalid progression", []int{1, 2, 4}, false},
		{"Empty array", []int{}, true},
		{"Single element", []int{5}, true},
		{"Two elements", []int{1, 2}, true},
		{"Negative numbers", []int{-3, -1, 1}, true},
		{"Same numbers", []int{2, 2, 2, 2}, true},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			result := isArithmeticProgression(tc.input)
			if result != tc.expected {
				t.Errorf("isArithmeticProgression(%v) = %v; want %v", tc.input, result, tc.expected)
			}
		})
	}
}
// Simple implementation tests:1 ends here
