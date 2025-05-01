use proc_macro::TokenStream;
use quote::quote;
use syn::{parse_macro_input, DeriveInput};

/// Derives the `BytableCommand` trait for a struct that contains a field named `command`.
/// Assumes the `command` field itself implements `Bytable`.
#[proc_macro_derive(BytableCommand)]
pub fn derive_bytable(input: TokenStream) -> TokenStream {
    // Parse the input tokens into a syntax tree
    let input = parse_macro_input!(input as DeriveInput);

    // Get the name of the struct we're deriving for
    let name = input.ident;

    // Build the output token stream
    let expanded = quote! {
        impl Bytable for #name {
            fn to_bytes(&self) -> Vec<u8> {
                self.command.to_bytes()
            }
        }
    };

    TokenStream::from(expanded)
}

#[proc_macro_derive(DefaultableCommand)]
pub fn derive_defaultable(input: TokenStream) -> TokenStream {
    // Parse the input tokens into a syntax tree
    let input = parse_macro_input!(input as DeriveInput);

    // Get the name of the struct we're deriving for
    let name = input.ident;

    // Build the output token stream
    let expanded = quote! {
        impl Default for #name {
            fn default() -> Self {
                Self::new()
            }
        }
    };

    TokenStream::from(expanded)
}

#[proc_macro_derive(Registrable)]
pub fn derive_registrable(input: TokenStream) -> TokenStream {
    // Parse the input tokens into a syntax tree
    let input = parse_macro_input!(input as DeriveInput);

    // Get the name of the struct we're deriving for
    let name = input.ident;

    // Build the output token stream
    let expanded = quote! {
        impl Registrable for #name {
            fn register(&self) -> Register {
                self.register
            }
        }
    };

    TokenStream::from(expanded)
}

#[proc_macro_derive(RegistrableCommand)]
pub fn derive_registrable_command(input: TokenStream) -> TokenStream {
    // Parse the input tokens into a syntax tree
    let input = parse_macro_input!(input as DeriveInput);

    // Get the name of the struct we're deriving for
    let name = input.ident;

    // Build the output token stream
    let expanded = quote! {
        impl Registrable for #name {
            fn register(&self) -> Register {
                self.command.register()
            }
        }
    };

    TokenStream::from(expanded)
}

#[proc_macro_derive(BytableRegistrable)]
pub fn derive_bytable_registrable(input: TokenStream) -> TokenStream {
    // Parse the input tokens into a syntax tree
    let input = parse_macro_input!(input as DeriveInput);

    // Get the name of the struct we're deriving for
    let name = input.ident;

    // Build the output token stream
    let expanded = quote! {

        impl Bytable for #name {
            fn to_bytes(&self) -> Vec<u8> {
                self.to_bytes()
            }
        }

        impl Registrable for #name {
            fn register(&self) -> Register {
                self.register()
            }
        }

        impl BytableRegistrable for #name {}
    };

    TokenStream::from(expanded)
}

#[proc_macro_derive(BytableRegistrableCommand)]
pub fn derive_bytable_registrable_command(input: TokenStream) -> TokenStream {
    // Parse the input tokens into a syntax tree
    let input = parse_macro_input!(input as DeriveInput);

    // Get the name of the struct we're deriving for
    let name = input.ident;

    // Build the output token stream
    let expanded = quote! {
        impl Bytable for #name {
            fn to_bytes(&self) -> Vec<u8> {
                self.command.to_bytes()
            }
        }

        impl Registrable for #name {
            fn register(&self) -> Register {
                self.command.register()
            }
        }

        impl BytableRegistrable for #name {}
    };

    TokenStream::from(expanded)
}
