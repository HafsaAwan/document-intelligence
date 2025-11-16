// types.d.ts

/**
 * This declaration silences the TypeScript error (TS7016)
 * for the 'react-simple-icons' package which does not
 * ship with its own type definitions.
 */
declare module 'react-simple-icons' {
  // You can define a more specific type if needed, but for quick fix:
  const content: any;
  export = content;
}