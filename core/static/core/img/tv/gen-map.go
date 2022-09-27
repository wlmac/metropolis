package main

import (
	_ "embed"
	"html/template"
	"log"
	"os"
	"strings"

	"github.com/hashicorp/hcl/v2/hclsimple"
)

//go:embed map.tmpl.svg
var tmpl string

type Data struct {
	Groups []Group `hcl:"group,block"`
}

type Group struct {
	Name   string `hcl:"name,label"`
	X      int    `hcl:"x"`
	Y      int    `hcl:"y"`
	Rotate int    `hcl:"rotate,optional"`
	Colour string `hcl:"colour"`

	Desks []Desk `hcl:"desk,block"`
}

type Desk struct {
	Name   string `hcl:"name,label"`
	X      int    `hcl:"x"`
	Y      int    `hcl:"y"`
	Rotate int    `hcl:"rotate,optional"`
}

func main() {
	var data Data
	err := hclsimple.DecodeFile("data.hcl", nil, &data)
	if err != nil {
		log.Fatalf("load config: %s", err)
	}
	t := template.New("")
	t.Funcs(template.FuncMap{
		"add":    func(x, y int) int { return x + y },
		"negate": func(x int) int { return -x },
		"stats": func(s string) []string {
			return strings.Split(s, "-")
		},
	})
	template.Must(t.Parse(tmpl))
	err = t.Execute(os.Stdout, data)
	if err != nil {
		log.Fatalf("execute: %s", err)
	}
}
